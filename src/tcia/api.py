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
import os

from tcia import _resources


__all__ = ["Client"]


class Client:
    def __init__(
        self,
        api_key=None,
        *,
        base_url="https://services.cancerimagingarchive.net/services/v3",
    ):
        if api_key is None:
            try:
                api_key = os.environ["TCIA_API_KEY"]
            except KeyError:
                raise TypeError(
                    (
                        "environmental variable 'TCIA_API_KEY' must be set or "
                        "keyword argument 'api_key' must not be None"
                    )
                )
        self._api_key = api_key
        self._base_url = base_url

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._api_key}')"

    @property
    def api_key(self):
        return self._api_key

    @property
    def base_url(self):
        return self._base_url

    @property
    def collections(self):
        return _resources.CollectionsResource(self.api_key, self.base_url)

    @property
    def modalities(self):
        return _resources.ModalitiesResource(self.api_key, self.base_url)

    @property
    def body_parts_examined(self):
        return _resources.BodyPartsExaminedResource(
            self.api_key, self.base_url
        )

    @property
    def manufacturers(self):
        return _resources.ManufacturersResource(self.api_key, self.base_url)

    @property
    def patients(self):
        return _resources.PatientsResource(self.api_key, self.base_url)

    @property
    def patients_by_modality(self):
        return _resources.PatientsByModalityResource(
            self.api_key, self.base_url
        )

    @property
    def patient_studies(self):
        return _resources.PatientStudiesResource(self.api_key, self.base_url)

    @property
    def series(self):
        return _resources.SeriesResource(self.api_key, self.base_url)

    @property
    def series_size(self):
        return _resources.SeriesSizeResource(self.api_key, self.base_url)

    @property
    def images(self):
        return _resources.ImagesResource(self.api_key, self.base_url)

    @property
    def new_patients_in_collection(self):
        return _resources.NewPatientsInCollectionResource(
            self.api_key, self.base_url
        )

    @property
    def new_studies_in_patient_collection(self):
        return _resources.NewStudiesInPatientCollectionResource(
            self.api_key, self.base_url
        )

    @property
    def sop_instance_uids(self):
        return _resources.SOPInstanceUIDsResource(self.api_key, self.base_url)

    @property
    def single_image(self):
        return _resources.SingleImageResource(self.api_key, self.base_url)

    @property
    def contents_by_name(self):
        return _resources.ContentsByNameResource(self.api_key, self.base_url)
