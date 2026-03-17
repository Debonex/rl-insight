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

"""Base data definitions for RL-Insight."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, List, Optional


class DataValidationError(Exception):
    """Exception raised when data validation fails."""

    def __init__(self, message: str, errors: Optional[List[str]] = None):
        super().__init__(message)
        self.errors = errors or []

    def __str__(self) -> str:
        if self.errors:
            return f"{super().__str__()}\n  - " + "\n  - ".join(self.errors)
        return super().__str__()


@dataclass
class ValidationResult:
    """Validation result"""

    is_valid: bool
    errors: List[str] = field(default_factory=list)

    def raise_if_invalid(self) -> None:
        if not self.is_valid:
            raise DataValidationError("Data validation failed", self.errors)

    def __bool__(self) -> bool:
        return self.is_valid


class ValidationRule(ABC):
    """Validation rule base class"""

    @abstractmethod
    def check(self, data: Any) -> bool:
        pass

    @property
    @abstractmethod
    def error_message(self) -> str:
        pass


class BaseValidator:
    """Base validator class"""

    def __init__(self):
        self._rules: List[ValidationRule] = []

    def add_rule(self, rule: ValidationRule) -> "BaseValidator":
        """Add a validation rule"""
        self._rules.append(rule)
        return self

    def validate(self, data: Any) -> ValidationResult:
        """Validate the data against all rules and return a ValidationResult"""
        errors = []

        for rule in self._rules:
            try:
                if not rule.check(data):
                    errors.append(rule.error_message)
            except Exception as e:
                errors.append(f"Validation rule execution failed: {e}")

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
        )


class BaseData:
    """Base data class for RL-Insight."""

    def __init__(self, validator: Optional[BaseValidator] = None):
        self._validator = validator

    def check(self) -> ValidationResult:
        """Validate the data"""
        return (
            self._validator.validate(self)
            if self._validator
            else ValidationResult(is_valid=True)
        )

    def check_or_raise(self) -> None:
        """Raise an exception if validation fails"""
        self.check().raise_if_invalid()

    @property
    def is_valid(self) -> bool:
        return self.check().is_valid
