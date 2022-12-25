from typing import Generic, TypeVar

from pydantic import BaseModel
from requests import Response as RequestsResponse

ResponseModel = TypeVar("ResponseModel", bound=BaseModel)


class Response(RequestsResponse, Generic[ResponseModel]):
    def __init__(self, *args, response_model: type[ResponseModel] | None = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.response_model = response_model

    def dataclass(self) -> ResponseModel:
        self.raise_for_status()

        if self.response_model is None:
            raise ValueError(
                "response_model must be non-null if you wish to use dataclass(). Did you forget to set it?"
            )

        return self.response_model.parse_raw(self.content)
