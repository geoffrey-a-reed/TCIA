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
import requests


__all__ = [
    "get_text",
    "get_content_iter",
    "write_text",
    "write_streaming_content",
]


def _filter_none_from_dict(dict_):
    return {key: value for key, value in dict_.items() if value is not None}


def get_text(url, *, headers=None, params=None):
    if headers is None:
        headers = {}

    if params is None:
        params = {}

    headers = _filter_none_from_dict(headers)
    params = _filter_none_from_dict(params)

    response = requests.get(url, headers=headers, params=params)
    return response.text


def get_content_iter(url, *, headers=None, params=None, chunk_size=1024):
    if not chunk_size > 0:
        raise ValueError("chunk size in bytes must be greater than zero")

    if headers is None:
        headers = {}

    if params is None:
        params = {}

    headers = _filter_none_from_dict(headers)
    params = _filter_none_from_dict(params)

    response = requests.get(url, headers=headers, params=params, stream=True)
    return response.iter_content(chunk_size=chunk_size)


def write_text(text, path_or_buffer, *, mode="wt", encoding="utf-8"):
    try:
        path_or_buffer.write(text)
    except AttributeError:
        with open(path_or_buffer, mode=mode, encoding=encoding) as buffer:
            buffer.write(text)
    else:
        path_or_buffer.flush()


def write_streaming_content(content_iter, path_or_buffer, *, mode="wb"):
    bytes_ = next(content_iter)

    try:
        path_or_buffer.write(bytes_)
    except AttributeError:
        with open(path_or_buffer, mode=mode) as buffer:
            buffer.write(bytes_)

            for bytes_ in content_iter:
                buffer.write(bytes_)
    else:
        for bytes_ in content_iter:
            buffer.write(bytes_)

        buffer.flush()
