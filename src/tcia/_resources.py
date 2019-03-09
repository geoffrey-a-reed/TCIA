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

    _required_params = []

    def __init__(self, api_key, base_url, *, resource, endpoint):
        self._api_key = api_key
        self._base_url = base_url
        self._resource = resource
        self._endpoint = endpoint
        self._headers = {"api_key": api_key}
        self._url = f"{base_url}/{resource}/query/{endpoint}"
        self._params = {}
        self._metadata = None

    def __repr__(self):
        return (
            f"{self.__class__.__name__}('{self._api_key}', '{self._base_url}', "
            f"resource='{self._resource}'', endpoint='{self._endpoint}')"
        )

    def __call__(self):
        return self

    @classmethod
    def _check_required_params(cls, params):
        for param in cls._required_params:
            if params.get(param) is None:
                raise TypeError(
                    f"required param '{param}' must be set using "
                    f"{cls.__name__}().__call__() prior to call to "
                    f"{cls.__name__}().get() or {cls.__name__}().download()"
                )

    @property
    def metadata(self):
        if self._metadata is None:
            url = f"{self._url}/metadata"
            text = _utils.get_text(url, headers=self._headers)
            data = json.loads(text)
            metadata = _types.Metadata(
                query_name=data["QueryName"],
                description=data["Description"],
                parameters=[param for param in data["Parameters"]],
                result=_types.Result(
                    name=data["Result"]["Name"],
                    description=data["Result"]["Description"],
                    attributes=[
                        _types.Attribute(
                            name=attr["Name"],
                            description=attr["Description"],
                            dicom=attr["DICOM"],
                        )
                        for attr in data["Result"]["Attributes"]
                    ],
                ),
            )
            self._metadata = metadata
        return self._metadata


class _TextResource(_Resource):

    _formats = ["csv", "html", "xml", "json"]
    _required_params = []

    @classmethod
    def _check_format(cls, format_):
        if not format_ in cls._formats:
            raise TypeError(
                f"invalid format_ '{format_}': try one of {cls._formats}"
            )

    def get(self):
        self.__class__._check_required_params(self._params)
        self._params.update({"format": "json"})
        text = _utils.get_text(
            self._url, headers=self._headers, params=self._params
        )
        data = json.loads(text)
        return data

    def download(
        self, path_or_buffer, format_="csv", *, mode="wt", encoding="utf-8"
    ):
        self.__class__._check_required_params(self._params)
        self.__class__._check_format(format_)
        self._params.update({"format": format_})
        text = _utils.get_text(
            self._url, headers=self._headers, params=self._params
        )
        _utils.write_text(text, path_or_buffer, mode=mode, encoding=encoding)


class _BytesResource(_Resource):

    _required_params = []

    def download(self, path_or_buffer, chunk_size=1024, *, mode="wb"):
        self.__class__._check_required_params(self._params)
        content_iter = _utils.get_content_iter(
            self._url,
            headers=self._headers,
            params=self._params,
            chunk_size=chunk_size,
        )
        _utils.write_streaming_content(content_iter, path_or_buffer, mode=mode)


class CollectionsResource(_TextResource):
    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="TCIA",
        endpoint="getCollectionValues",
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def get(self):
        data = super().get()
        collections = [
            _types.Collection(collection=element.get("Collection"))
            for element in data
        ]
        return collections


class ModalitiesResource(_TextResource):
    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="TCIA",
        endpoint="getModalityValues",
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, collection=None, body_part_examined=None):
        self._params.update(
            {"Collection": collection, "BodyPartExamined": body_part_examined}
        )
        return self

    def get(self):
        data = super().get()
        modalities = [
            _types.Modality(modality=element.get("Modality"))
            for element in data
        ]
        return modalities


class BodyPartsExaminedResource(_TextResource):
    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="TCIA",
        endpoint="getBodyPartValues",
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, collection=None, modality=None):
        self._params.update({"Collection": collection, "Modality": modality})
        return self

    def get(self):
        data = super().get()
        body_parts_examined = [
            _types.BodyPartExamined(
                body_part_examined=element.get("BodyPartExamined")
            )
            for element in data
        ]
        return body_parts_examined


class ManufacturersResource(_TextResource):
    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="TCIA",
        endpoint="getManufacturerValues",
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(
        self, *, collection=None, modality=None, body_part_examined=None
    ):
        self._params.update(
            {
                "Collection": collection,
                "Modality": modality,
                "BodyPartExamined": body_part_examined,
            }
        )
        return self

    def get(self):
        data = super().get()
        manufacturers = [
            _types.Manufacturer(manufacturer=element.get("Manufacturer"))
            for element in data
        ]
        return manufacturers


class PatientsResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getPatient"
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, collection=None):
        self._params.update({"Collection": collection})
        return self

    def get(self):
        data = super().get()
        patients = [
            _types.Patient(
                patient_id=element.get("PatientID"),
                patient_name=element.get("PatientName"),
                patient_sex=element.get("PatientSex"),
                collection=element.get("Collection"),
            )
            for element in data
        ]
        return patients


class PatientsByModalityResource(_TextResource):

    _required_params = ["Collection", "Modality"]

    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="TCIA",
        endpoint="PatientsByModality",
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, collection, modality):
        self._params.update({"Collection": collection, "Modality": modality})
        return self

    def get(self):
        data = super().get()
        patient_by_modality = [
            _types.PatientByModality(
                patient_id=element.get("PatientID"),
                patient_name=element.get("PatientName"),
                patient_sex=element.get("PatientSex"),
                collection=element.get("Collection"),
            )
            for element in data
        ]
        return patients


class PatientStudiesResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getPatientStudy"
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(
        self, *, collection=None, patient_id=None, study_instance_uid=None
    ):
        self._params.update(
            {
                "Collection": collection,
                "PatientID": patient_id,
                "StudyInstanceUID": study_instance_uid,
            }
        )
        return self

    def get(self):
        data = super().get()
        patient_studies = [
            _types.PatientStudy(
                study_instance_uid=element.get("StudyInstanceUID"),
                study_date=element.get("StudyDate"),
                study_description=element.get("StudyDescription"),
                patient_age=element.get("PatientAge"),
                patient_id=element.get("PatientID"),
                patient_name=element.get("PatientName"),
                patient_sex=element.get("PatientSex"),
                collection=element.get("Collection"),
                series_count=element.get("SeriesCount"),
            )
            for element in data
        ]
        return patient_studies


class SeriesResource(_TextResource):
    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getSeries"
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(
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
        return self

    def get(self):
        data = super().get()
        series_list = [
            _types.Series(
                series_instance_uid=element.get("SeriesInstanceUID"),
                study_instance_uid=element.get("StudyInstanceUID"),
                modality=element.get("Modality"),
                protocol_name=element.get("ProtocolName"),
                series_date=element.get("SeriesDate"),
                series_description=element.get("SeriesDescription"),
                body_part_examined=element.get("BodyPartExamined"),
                series_number=element.get("SeriesNumber"),
                annotations_flag=element.get("AnnotationsFlag"),
                collection=element.get("Collection"),
                patient_id=element.get("PatientID"),
                manufacturer=element.get("Manufacturer"),
                manufacturer_model_name=element.get("ManufacturerModelName"),
                software_version=element.get("SoftwareVersion"),
                image_count=element.get("ImageCount"),
            )
            for element in data
        ]
        return series_list


class SeriesSizeResource(_TextResource):

    _required_params = ["SeriesInstanceUID"]

    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getSeriesSize"
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, series_instance_uid):
        self._params.update({"SeriesInstanceUID": series_instance_uid})
        return self

    def get(self):
        data = super().get()
        series_sizes = [
            _types.SeriesSize(
                total_size_in_bytes=element.get("TotalSizeInBytes"),
                object_count=element.get("ObjectCount"),
            )
            for element in data
        ]
        return series_sizes


class ImagesResource(_BytesResource):

    _required_params = ["SeriesInstanceUID"]

    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getImage"
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, series_instance_uid):
        self._params.update({"SeriesInstanceUID": series_instance_uid})
        return self


class NewPatientsInCollectionResource(_TextResource):

    _required_params = ["Date", "Collection"]

    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="TCIA",
        endpoint="NewPatientsInCollection",
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, date, collection):
        self._params.update({"Date": date, "Collection": collection})
        self._configured = True
        return self

    def get(self):
        data = super().get()
        new_patients_in_collection = [
            _types.NewPatientInCollection(
                patient_id=element.get("PatientID"),
                collection=element.get("Collection"),
            )
            for element in data
        ]
        return new_patients_in_collection


class NewStudiesInPatientCollectionResource(_TextResource):

    _required_params = ["Date", "Collection"]

    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="TCIA",
        endpoint="NewStudiesInPatientCollection",
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, date, collection, patient_id=None):
        self._params.update(
            {"Date": date, "Collection": collection, "PateintID": patient_id}
        )
        return self

    def get(self):
        data = super().get()
        new_studies_in_patient_collection = [
            _types.NewStudyInPatientCollection(
                patient_id=element.get("PatientID"),
                collection=element.get("Collection"),
                study_instance_uid=element.get("StudyInstanceUID"),
            )
            for element in data
        ]
        return new_studies_in_patient_collection


class SOPInstanceUIDsResource(_TextResource):

    _required_params = ["SeriesInstanceUID"]

    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="TCIA",
        endpoint="getSOPInstanceUIDs",
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, series_instance_uid):
        self._params.update({"SeriesInstanceUID": series_instance_uid})
        return self

    def get(self):
        data = super().get()
        sop_instance_uids = [
            _types.SOPInstanceUID(
                # API documentation inconsistent: "sop_instance_uid" not
                #   "SOPInstanceUID". Reason unknown.
                sop_instance_uid=element.get("sop_instance_uid")
            )
            for element in data
        ]
        return sop_instance_uids


class SingleImageResource(_BytesResource):

    _required_params = ["SeriesInstanceUID", "SOPInstanceUID"]

    def __init__(
        self, api_key, base_url, *, resource="TCIA", endpoint="getSingleImage"
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, series_instance_uid, sop_instance_uid):
        self._params.update(
            {
                "SeriesInstanceUID": series_instance_uid,
                "SOPInstanceUID": sop_instance_uid,
            }
        )
        return self


class ContentsByNameResource(_TextResource):

    _required_params = ["name"]

    def __init__(
        self,
        api_key,
        base_url,
        *,
        resource="SharedList",
        endpoint="ContentsByName",
    ):
        super().__init__(
            api_key, base_url, resource=resource, endpoint=endpoint
        )

    def __call__(self, *, name):
        self._params.update({"name": name})
        return self

    def get(self):
        data = super().get()
        return data
