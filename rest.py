#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, render_template_string
from flask_restx import Api, Resource, fields
from pydantic import BaseModel

from configs import ConfigurationManager
from playlist_downloader import playlist_download
from single_downloader import single_download
from system_utils import ProgramExecutionDto
from updater import update


class RestResponseDto(BaseModel):
    data: dict
    success: bool = True
    message: str = "OK"


_cfg: ConfigurationManager = ConfigurationManager()

app = Flask(__name__)

@app.route('/')
def index():
    """Serves the simple homepage webpage"""
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📺 Youtube-DL bindings</title>
</head>
<body>
    <h1>📺 Youtube-DL bindings web page</h1>
    <h3>Welcome to the Youtube-DL bindings web page</h1>
    <p>Click the link below to view the interactive API documentation.</p>
    <a href="/swagger">Go to Swagger UI</a>
</body>
</html>
    """.strip()
    return render_template_string(html)


api = Api(
    app,
    version='1.0',
    title='Youtube-DL bindings API',
    description='Youtube-DL bindings interactive API demonstration',
    doc='/swagger'
)
ns = api.namespace('api', description='Main operations')


# --- Explicit Flask-Restx Swagger Models ---

rest_response_model = api.model('RestResponseDto', {
    'data': fields.Raw(default=dict(), description='Data'),
    'success': fields.Boolean(default=True),
    'message': fields.String(default="OK")
})

# Request payload validation models for POST endpoints
set_int_model = api.model('SetIntRequest', {
    'value': fields.Integer(required=True, description='New integer value', min=1)
})

set_string_model = api.model('SetStringRequest', {
    'value': fields.String(required=True, description='New string value', min_length=1)
})


# --- Shared State Setter Wrapper ---

# =========================================================================
# Endpoints for fetch_max_attempts
# =========================================================================


@ns.route('/config/get-fetch-max-attempts')
class GetFetchMaxAttempts(Resource):
    @api.doc(description='Getter for fetch_max_attempts. Returns a raw integer.')
    @api.response(200, 'Success', fields.Integer)
    def get(self):
        return _cfg.get_fetch_max_attempts(), 200


@ns.route('/config/set-fetch-max-attempts')
class SetFetchMaxAttempts(Resource):
    @api.expect(set_int_model, validate=True)
    @api.marshal_with(rest_response_model, code=200)
    @api.doc(description='Setter for fetch_max_attempts. Returns RestResponseDto JSON.')
    def post(self):
        new_value = request.json.get('value')
        _cfg.set_fetch_max_attempts(value=new_value)
        dto: RestResponseDto = RestResponseDto(data={'fetch_max_attempts': new_value})
        return dto.model_dump(), 200


# =========================================================================
# Endpoints for fetch_max_delay_seconds
# =========================================================================


@ns.route('/config/get-fetch-max-delay-seconds')
class GetFetchMaxDelaySeconds(Resource):
    @api.doc(description='Getter for fetch_max_delay_seconds. Returns a raw integer.')
    @api.response(200, 'Success', fields.Integer)
    def get(self):
        return _cfg.get_fetch_max_delay_seconds(), 200


@ns.route('/config/set-fetch-max-delay-seconds')
class SetFetchMaxDelaySeconds(Resource):
    @api.expect(set_int_model, validate=True)
    @api.marshal_with(rest_response_model, code=200)
    @api.doc(description='Setter for fetch_max_delay_seconds. Returns RestResponseDto JSON.')
    def post(self):
        new_value = request.json.get('value')
        _cfg.set_fetch_max_delay_seconds(value=new_value)
        dto: RestResponseDto = RestResponseDto(data={'fetch_max_delay_seconds': new_value})
        return dto.model_dump(), 200


# =========================================================================
# Endpoints for single_download_template
# =========================================================================


@ns.route('/config/get-single-download-template')
class GetSingleDownloadTemplate(Resource):
    @api.doc(description='Getter for single_download_template. Returns a raw string.')
    @api.response(200, 'Success', fields.String)
    def get(self):
        return _cfg.get_single_download_template(), 200


@ns.route('/config/set-single-download-template')
class SetSingleDownloadTemplate(Resource):
    @api.expect(set_string_model, validate=True)
    @api.marshal_with(rest_response_model, code=200)
    @api.doc(description='Setter for single_download_template. Returns RestResponseDto JSON.')
    def post(self):
        new_value = request.json.get('value')
        _cfg.set_single_download_template(new_value)
        dto: RestResponseDto = RestResponseDto(data={'single_download_template': new_value})
        return dto.model_dump(), 200


# =========================================================================
# Endpoints for playlist_download_template
# =========================================================================


@ns.route('/config/get-playlist-download-template')
class GetPlaylistDownloadTemplate(Resource):
    @api.doc(description='Getter for playlist_download_template. Returns a raw string.')
    @api.response(200, 'Success', fields.String)
    def get(self):
        return _cfg.get_playlist_download_template(), 200


@ns.route('/config/set-playlist-download-template')
class SetPlaylistDownloadTemplate(Resource):
    @api.expect(set_string_model, validate=True)
    @api.marshal_with(rest_response_model, code=200)
    @api.doc(description='Setter for playlist_download_template. Returns RestResponseDto JSON.')
    def post(self):
        new_value = request.json.get('value')
        _cfg.set_playlist_download_template(new_value)
        dto: RestResponseDto = RestResponseDto(data={'playlist_download_template': new_value})
        return dto.model_dump(), 200


# =========================================================================
# Endpoints for updater
# =========================================================================


@ns.route('/update')
class UpdateEndpoint(Resource):
    @api.marshal_with(rest_response_model, code=200)
    @api.doc(description='Update')
    def get(self):
        _ = update()
        dto: RestResponseDto = RestResponseDto(data=dict())
        return dto.model_dump(), 200


# =========================================================================
# Endpoints for single_downloader
# =========================================================================


download_model = api.model('DownloadRequest', {
    'url': fields.String(required=True, description='URL', min_length=1),
    'directory': fields.String(required=True, description='Directory', min_length=1),
})

@ns.route('/download/single-download')
class SingleDownloadEndpoint(Resource):
    @api.expect(download_model, validate=True)
    @api.marshal_with(rest_response_model, code=200)
    @api.doc(description='Single download')
    def post(self):
        url = request.json.get('url')
        directory = request.json.get('directory')
        _ = single_download(url=url, directory=directory)
        dto: RestResponseDto = RestResponseDto(data=dict())
        return dto.model_dump(), 200


# =========================================================================
# Endpoints for playlist_downloader
# =========================================================================


@ns.route('/download/playlist-download')
class PlaylistDownloadEndpoint(Resource):
    @api.expect(download_model, validate=True)
    @api.marshal_with(rest_response_model, code=200)
    @api.doc(description='Playlist download')
    def post(self):
        url = request.json.get('url')
        directory = request.json.get('directory')
        execution_dto: ProgramExecutionDto = playlist_download(playlist_url=url, directory=directory)
        response_dto: RestResponseDto = RestResponseDto(data=execution_dto.model_dump())
        return response_dto.model_dump(), 200


def run():
    app.run(
        host="0.0.0.0",
        port=8090,
        debug=False,
    )


if __name__ == '__main__':
    run()
