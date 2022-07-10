from .movie import MoviesApi, MovieApi
from .auth import LoginPasien, SignupApi, LoginApi, DaftarPasien
from .reset_password import ForgotPassword, ResetPassword

def initialize_routes(api):
    api.add_resource(DaftarPasien, '/pasien/register')
    api.add_resource(LoginPasien, '/pasien/login')

    api.add_resource(MoviesApi, '/api/movies')
    api.add_resource(MovieApi, '/api/movies/<id>')

    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')

    api.add_resource(ForgotPassword, '/api/auth/forgot')
    api.add_resource(ResetPassword, '/api/auth/reset')
