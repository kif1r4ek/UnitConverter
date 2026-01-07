from fastapi.templating import Jinja2Templates
from pint import UnitRegistry

templates = Jinja2Templates(directory="app/views/templates")

ureg = UnitRegistry()