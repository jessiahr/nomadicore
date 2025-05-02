from fastapi import FastAPI
app = FastAPI()
import ui
ui.init(app)
