from pydantic import BaseModel

def to_camel_case(arg: str) -> str:
    string_split = arg.split("_")
    return string_split[0] + "".join(word.capitalize() for word in string_split[1:])


class SmartixModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        use_enum_values = True
        arbitrary_types_allowed = True