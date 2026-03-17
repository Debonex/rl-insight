# Copyright (c) 2025 verl-project authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional

from rl_insight.data.base import ValidationRule


class PathExistsRule(ValidationRule):
    def check(self, data) -> bool:
        return data.path.exists()

    @property
    def error_message(self, path: Optional[str] = None) -> str:
        return (
            f"Source path does not exist: {path}"
            if path
            else "Source path does not exist"
        )
