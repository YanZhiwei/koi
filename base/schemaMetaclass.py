from typing import Any

from pydantic import BaseModel


class SchemaMetaclass(BaseModel):
    def __init__(self, **data: Any):
        super().__init__(**data)
        # 获取 ORM 模型属性
        model_attrs = get_orm_model_recursive(self.__class__.__annotations__, self.__class__.__bases__)
        if model_attrs:
            for key, schema_attr_field in self.__annotations__.items():
                if hasattr(model_attrs, key):
                    model_attr = getattr(model_attrs, key)
                    if hasattr(self.__fields__[key], 'field_info'):
                        field_info = self.__fields__[key].field_info
                        # 更新 description，使用 ORM 模型中的评论信息
                        description = (
                            (field_info.description or "") + "<br/>" + model_attr.property.columns[0].comment
                        ) if hasattr(model_attr.property.columns[0], 'comment') else field_info.description
                        self.__fields__[key].field_info.description = description
    
def get_orm_model_recursive(current_attrs, current_bases):
    if current_attrs.get("Config"):
        return current_attrs.get("Config").orm_model
    bases = get_base_classes_recursive(current_bases[0], [current_bases[0]])
    for base in bases:
        if getattr(base, "Config", None) and getattr(base.Config, "orm_model", None):
            return base.Config.orm_model
    return None

def get_base_classes_recursive(specified_class, base_class_result=(), stop_name="object"):
    base_classes = specified_class.__bases__
    for base in base_classes:
        base_name = base.__name__
        if base_name != stop_name:
            base_class_result.append(base)
        elif base_name == "object":
            base_class_result.append(object)
            return base_class_result
    return get_base_classes_recursive(base, base_class_result, stop_name)