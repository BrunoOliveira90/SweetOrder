from flask import render_template, redirect, session, url_for, Blueprint, flash, request
from .models import Order, OrderItem, Product, User, UpdateProfileForm
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

