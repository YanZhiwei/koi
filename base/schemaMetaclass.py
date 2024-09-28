from pydantic.main import ModelMetaclass


class SchemaMetaclass(ModelMetaclass):
    def __new__(mcs, name, bases, attrs):
        schema_attrs = attrs["__annotations__"]
        model_attrs = get_orm_model_recursive(attrs, bases)
        if not model_attrs:
            return ModelMetaclass.__new__(mcs, name, bases, attrs)
        for key in schema_attrs:
            if not hasattr(model_attrs, key):
                continue
            model_attr = getattr(model_attrs, key)
            schema_attr_field = attrs.get(key)
            if schema_attr_field.description:
                description = schema_attr_field.description + "<br/>" + model_attr.property.columns[0].comment
            else:
                description = model_attr.property.columns[0].comment
            setattr(schema_attr_field, "description", description)
        return ModelMetaclass.__new__(mcs, name, bases, attrs)
    
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