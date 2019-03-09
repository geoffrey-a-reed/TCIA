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


__all__ = [
    "Attribute",
    "BodyPartExamined",
    "Collection",
    "Manufacturer",
    "Metadata",
    "Modality",
    "Patient",
    "PatientStudy",
    "Result",
    "Series",
]

Collection = collections.namedtuple("Collection", ["collection"])

Modality = collections.namedtuple("Modality", ["modality"])

BodyPartExamined = collections.namedtuple(
    "BodyPartExamined", ["body_part_examined"]
)

Manufacturer = collections.namedtuple("Manufacturer", ["manufacturer"])

Metadata = collections.namedtuple(
    "Metadata", ["query_name", "description", "parameters", "result"]
)

Result = collections.namedtuple(
    "Result", ["name", "description", "attributes"]
)

Attribute = collections.namedtuple(
    "Attribute", ["name", "description", "dicom"]
)

Patient = collections.namedtuple(
    "Patient", ["patient_id", "patient_name", "patient_sex", "collection"]
)

PatientByModality = collections.namedtuple(
    "PatientByModality", ["id_", "collection", "modality"]
)

PatientStudy = collections.namedtuple(
    "PatientStudy",
    [
        "study_instance_uid",
        "study_date",
        "study_description",
        "patient_age",
        "patient_id",
        "patient_name",
        "patient_sex",
        "collection",
        "series_count",
    ],
)

Series = collections.namedtuple(
    "Series",
    [
        "series_instance_uid",
        "study_instance_uid",
        "modality",
        "protocol_name",
        "series_date",
        "series_description",
        "body_part_examined",
        "series_number",
        "annotations_flag",
        "collection",
        "patient_id",
        "manufacturer",
        "manufacturer_model_name",
        "software_version",
        "image_count",
    ],
)

SeriesSize = collections.namedtuple(
    "SeriesSize", ["total_size_in_bytes", "object_count"]
)

NewPatientInCollection = collections.namedtuple(
    "NewPatientInCollection", ["patient_id", "collection"]
)

NewStudyInPatientCollection = collections.namedtuple(
    "NewStudyInPatientCollection",
    ["patient_id", "collection", "study_instance_uid"],
)

SOPInstanceUID = collections.namedtuple("SOPInstanceUID", ["sop_instance_uid"])
