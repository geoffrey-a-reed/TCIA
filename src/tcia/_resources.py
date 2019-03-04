# Copyright 2019 Geoffrey A. Reed. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
# ----------------------------------------------------------------------
import json

from tcia import _errors
from tcia import _types
from tcia import _utils


__all__ = [
    "CollectionsResource",
    "ModalitiesResource",
    "BodyPartsResource",
    "ManufacturersResource",
    "PatientsResource",
    "PatientsByModalityResource",
    "PatientStudiesResource",
    "ImagesResource",
    "NewPatientsInCollectionResource",
    "NewStudiesInPatientCollectionResource",
    "SOPInstanceUIDsResource",
    "SingleImageResource",
    "ContentsByNameResource",
]


class _Resource:
    def __init__(self, api_key, base_url, *, resource, endpoint):
        self._api_key = api_key
        self._base_url = base_url
        self._resource = resource
        self._endpoint = endpoint
        self._headers = {"api_key": api_key}
        self._url = f"{base_url}/{resource}/query/{endpoint}"
        self._params = {}
        self._metadata = None
        self._configured = False

    def __repr__(self):
        return (
            f"{self.__class__.__name__}('{self._api_key}', '{self._base_url}', "
            f"resource='{self._resource}'', endpoint='{self._endpoint}')"
        )

    def configure(self):
        self._configured = True
        return self

    def _check_is_configured(self):
        if not self._configured:
            raise _errors.ConfigurationError(
                ".configure() must be called before .get() or .download()"
            )

    @property
    def metadata(self):
        if self._metadata is None:
            url = f"{self._url}/metadata"
            text = _utils.get_text(url, headers=self._headers)
            metadata = json.loads(text)
            self._metadata = metadata

        return self._metadata


class _TextResource(_Resource):

    _formats = ["csv", "html", "xml", "json"]

    @classmethod
    def _check_format(cls, format_):
        if not format_ in cls._formats:
            raise _errors.FormatError()

    def get(self):
        self._check_is_configured()

        self._params.update({"format": "json"})
        text = _utils.get_text(self._url, headers=self._headers, params=self._params)
        data = json.loads(text)
        return data

    def download(self, path_or_buffer, format_="csv", *, mode="wt", encoding="utf-8"):
        self._check_is_configured()
        self.__class__._check_format(format_)

        self._params.update({"format": format_})
        text = _utils.get_text(self._url, headers=self._headers, params=self._params)
        _utils.write_text(text, path_or_buffer, mode=mode, encoding=encoding)


class _BytesResource(_Resource):
    def download(self, path_or_buffer, chunk_size=1024, *, mode="wb"):
        self._check_is_configured()

        content_iter = _utils.get_content_iter(
            self._url, headers=self._headers, params=self._params, chunk_size=chunk_size
        )
        _utils.write_streaming_content(content_iter, path_or_buffer, mode=mode)


class CollectionsResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getCollectionValues"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def get(self):
        self._configured = True
        data = super().get()
        collections = [element.get("Collection") for element in data]
        return collections


class ModalitiesResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getModalityValues"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, collection=None, body_part_examined=None):
        self._params.update(
            {"Collection": collection, "BodyPartExamined": body_part_examined}
        )
        self._configured = True
        return self

    def get(self):
        self._configured = True
        data = super().get()
        modalities = [element.get("Modality") for element in data]
        return modalities


class BodyPartsResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getBodyPartValues"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, collection=None, modality=None):
        self._params.update({"Collection": collection, "Modality": modality})
        self._configured = True
        return self

    def get(self):
        self._configured = True
        data = super().get()
        body_parts = [element.get("BodyPartExamined") for element in data]
        return body_parts


class ManufacturersResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getManufacturerValues"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, collection=None, modality=None, body_part_examined=None):
        self._params.update(
            {
                "Collection": collection,
                "Modality": modality,
                "BodyPartExamined": body_part_examined,
            }
        )
        self._configured = True
        return self

    def get(self):
        self._configured = True
        data = super().get()
        manufacturers = [element.get("Manufacturer") for element in data]
        return manufacturers


class PatientsResource(_TextResource):
    def __init__(self, api_key, base_url, *, resource="TCIA", endpoint="getPatient"):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, collection=None):
        self._params.update({"Collection": collection})
        self._configured = True
        return self

    def get(self):
        self._configured = True
        data = super().get()
        patients = []
        for item in data:
            patient = _types.Patient(
                id_=item.get("PatientID"),
                name=item.get("PatientName"),
                sex=item.get("PatientSex"),
                collection=item.get("Collection")
            )
        return patients


class PatientsByModalityResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="PatientsByModality"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, collection, modality):
        self._params.update({"Collection": collection, "Modality": modality})
        self._configured = True
        return self

    def get(self):
        data = super().get()
        patients = []
        for item in data:
            patient = _types.Patient(
                id_=item.get("PatientID"),
                name=item.get("PatientName"),
                sex=item.get("PatientSex"),
                collection=item.get("Collection")
            )
            patients.append(patient)
        return patients


class PatientStudiesResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getPatientStudy"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, collection=None, patient_id=None, study_instance_uid=None):
        self._params.update(
            {
                "Collection": collection,
                "PatientID": patient_id,
                "StudyInstanceUID": study_instance_uid,
            }
        )
        self._configured = True
        return self

    def get(self):
        self._configured = True
        data = super().get()
        patient_studies = []
        for item in data:
            patient_study = _types.PatientStudy(
                patient_age=item.get("PatientAge"),
                patient_id=item.get("PatientID"),
                patient_name=item.get("PatientName"),
                patient_sex=item.get("PatientSex"),
                series_count=item.get("SeriesCount"),
                study_date=item.get("StudyDate"),
                study_description=item.get("StudyDescription"),
                study_instance_uid=item.get("StudyInstanceUID")
            )
            patient_studies.append(patient_study)
        return patient_studies


class SeriesResource(_TextResource):
    def __init__(self, api_key, base_url, *, resource="TCIA", endpoint="getSeries"):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(
        self,
        *,
        collection=None,
        study_instance_uid=None,
        patient_id=None,
        series_instance_uid=None,
        modality=None,
        manufacturer_model_name=None,
        manufacturer=None,
    ):
        self._params.update(
            {
                "Collection": collection,
                "StudyInstanceUID": study_instance_uid,
                "PatientID": patient_id,
                "SeriesInstanceUID": series_instance_uid,
                "Modality": modality,
                "ManufacturerModelName": manufacturer_model_name,
                "Manufacturer": manufacturer,
            }
        )
        self._configured = True
        return self
    
    def get(self):
        self._configured = True
        data = super().get()
        series_list = []
        for item in data:
            series = _types.Series(
                annotations_flag=item.get("AnnotationsFlag"),
                body_part_examined=item.get("BodyPartExamined"),
                collection=item.get("Collection"),
                image_count=item.get("ItemCount"),
                manufacturer=item.get("Manufacturer"),
                manufacturer_model_name=item.get("ManufacturerModelName"),
                modality=item.get("Modality"),
                protocol_name=item.get("ProtocolName"),
                series_date=item.get("SeriesDate"),
                series_description=item.get("SeriesDescription"),
                series_instance_uid=item.get("SeriesInstanceUID"),
                series_number=item.get("SeriesNumber"),
                software_version=item.get("SoftwareVersion"),
                study_instance_uid=item.get("StudyInstanceUID"),
                visibility=item.get("Visibility")
            )
            series_list.append(series)
        return series_list


class SeriesSizeResource(_TextResource):
    def __init__(self, api_key, base_url, *, resource="TCIA", endpoint="getSeriesSize"):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, series_instance_uid):
        self._params.update({"SeriesInstanceUID": series_instance_uid})
        self._configured = True
        return self

    def get(self):
        data = super().get()
        series_sizes = []
        for item in data:
            series_size = _types.SeriesSize(
                total_size_in_bytes=item.get("TotalSizeInBytes"),
                object_count=item.get("ObjectCount")
            )
            series_sizes.append(series_size)
        return series_sizes


class ImagesResource(_BytesResource):
    def __init__(self, api_key, base_url, *, resource="TCIA", endpoint="getImage"):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, series_instance_uid):
        self._params.update({"SeriesInstanceUID": series_instance_uid})
        self._configured = True
        return self


class NewPatientsInCollectionResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="NewPatientsInCollection"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, date, collection):
        self._params.update({"Date": date, "Collection": collection})
        self._configured = True
        return self
    
    def get(self):
        data = super().get()
        patients = []
        for item in data:
            patient = _types.Patient(
                id_=item.get("PatientID"),
                name=item.get("PatientName"),
                sex=item.get("PatientSex"),
                collection=item.get("Collection")
            )
            patients.append(patient)
        return patients


class NewStudiesInPatientCollectionResource(_TextResource):
    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="TCIA",
        endpoint="NewStudiesInPatientCollection",
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, date, collection, patient_id=None):
        self._params.update(
            {"Date": date, "Collection": collection, "PateintID": patient_id}
        )
        self._configured = True
        return self

    def get(self):
        data = super().get()
        patient_studies = []
        for item in data:
            patient_study = _types.PatientStudy(
                patient_age=item.get("PatientAge"),
                patient_id=item.get("PatientID"),
                patient_name=item.get("PatientName"),
                patient_sex=item.get("PatientSex"),
                series_count=item.get("SeriesCount"),
                study_date=item.get("StudyDate"),
                study_description=item.get("StudyDescription"),
                study_instance_uid=item.get("StudyInstanceUID")
            )
            patient_studies.append(patient_study)
        return patient_studies


class SOPInstanceUIDsResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getSOPInstanceUIDs"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, series_instance_uid):
        self._params.update({"SeriesInstanceUID": series_instance_uid})
        self._configured = True
        return self
    
    def get(self):
        self._configured = True
        data = super().get()
        sop_instance_uids = [item.get("SOPInstanceUID") for item in data]
        return sop_instance_uids


class SingleImageResource(_BytesResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getSingleImage"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, series_instance_uid, sop_instance_uid):
        self._params.update(
            {
                "SeriesInstanceUID": series_instance_uid,
                "SOPInstanceUID": sop_instance_uid,
            }
        )
        self._configured = True
        return self


class ContentsByNameResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="ContentsByName"
    ):
        super().__init__(api_key, base_url, resource=resource, endpoint=endpoint)

    def configure(self, *, name):
        self._params.update({"name": name})
        self._configured = True
        return self
    
    def get(self):
        data = super().get()
        return data
