from flask import request, make_response
from flask_restx import Resource

from api.CRUD.notation_queries import get_all_notations_of_user
from api.exceptions.errors import NotFoundError
from api.routes.edit import ns_edit, export_response_model_200, export_response_model_404
from api.routes.sleep import user_id_params
from api.utils.manage_notes import convert_notes, WriteData
from common.pydantic_schemas.sleep.notes import SleepNote
from common.pydantic_schemas.user import User


class EditRouteExport(Resource):
    @ns_edit.doc(description='Экспорт всех записей дневника сна в файл')
    @ns_edit.expect(user_id_params)
    @ns_edit.response(**export_response_model_200)
    @ns_edit.response(**export_response_model_404)
    def get(self):
        args = request.args.to_dict()
        user = User(**args)
        db_notes = get_all_notations_of_user(user.id)
        if not db_notes:
            raise NotFoundError
        notes: list[SleepNote] = convert_notes(db_notes, SleepNote)
        file_str: str = WriteData(notes).to_csv_str()
        response = make_response(file_str)
        response.status_code = 200
        response.mimetype = 'text/plain'
        response.headers.set(
            'Content-Disposition',
            'attachment',
            filename='sleep_diary.csv'
        )
        return response
