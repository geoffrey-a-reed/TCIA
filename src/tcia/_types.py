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
import collections


__all__ = ["Patient", "PatientStudy", "Series"]


Patient = collections.namedtuple(
    "Patient",
    ["id_", "name", "sex", "collection"]
)

PatientStudy = collections.namedtuple(
    "PatientStudy",
    [
        "patient_age",
        "patient_id",
        "patient_name",
        "patient_sex",
        "series_count",
        "study_date",
        "study_description",
        "study_instance_uid",
    ]
)

Series = collections.namedtuple(
    "Series",
    [
        "annotations_flag",
        "body_part_examined",
        "collection",
        "image_count",
        "manufacturer",
        "manufacturer_model_name",
        "modality",
        "protocol_name",
        "series_date",
        "series_description",
        "series_instance_uid",
        "series_number",
        "software_version",
        "study_instance_uid",
        "visibility",
    ]
)

SeriesSize = collections.namedtuple(
    "SeriesSize",
    [
        "total_size_in_bytes",
        "object_count",
    ]
)