"""
app.py - Streamlit App Principal
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px #Creación de gráficos
import plotly.graph_objects as go #Plotly Express sirve para crear gráficos interactivos de manera rápida
from datetime import datetime #Para manejar fechas y horas
import time #Para medir el tiempo o pausas
import sys #Sys permite interactuar con el sistema
import os #Para interactuar con archivos y carpetas del sistema

#Añadimos utils al path
sys.path.append(os.path.join(os.path.dirname(__file__),'utils'))

from utils.predictor import predictor
