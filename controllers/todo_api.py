import math
from urllib.parse import parse_qs

from odoo import http
from odoo.http import request
import json

    # Structure method valid response
def valid_response(data,pagination_info,status):
    response_body = {
    'message': 'Success',
    'data': data
    }
    if pagination_info:
        response_body['pagination'] = pagination_info

    return request.make_json_response(response_body,status= status)


    # Structure method invalid response
def invalid_response(error, status):
        response_body = {
            'error': error
        }
        return request.make_json_response(response_body,status= status)



class TODOApi(http.Controller):

    def _validate_required_fields(self, vals, fields):
        for field in fields:
            # check if field not sent or empty
            if not vals.get(field):
                return f"{field} is required"
        return None


    @http.route("/v1/todo",methods=["POST"],type="http",auth="none",csrf=False)
    def create_todo_api(self):
        try:
            args=request.httprequest.data.decode()
            vals=json.loads(args)

            required_fields=['task_name','assign_to']
            error = self._validate_required_fields(vals, required_fields)
            if error:
                return invalid_response(error, status=400)

            res=request.env['todo.task'].sudo().create(vals)
            if res:
                data ={
                "id":res.id,
                 "task_name":res.task_name,
                  "description":res.description,
                    "assign_to":res.assign_to,
                  }
                return valid_response(data,pagination_info=None, status=200)
            else:
                return invalid_response("Failed to create Todo", status=400)
        except Exception as e:
            return invalid_response(str(e), status=400)

    @http.route("/v1/Get_todo/<int:todo_id>",methods=["GET"],type="http",auth="none",csrf=False)
    def get_todo_api(self,todo_id):
        try:
            todo_id=request.env['todo.task'].sudo().search([('id','=',todo_id)])
            if not todo_id:
                return invalid_response("This ID not found", status=404)
            data = {
                "id": todo_id.id,
                "task_name": todo_id.task_name,
                "description": todo_id.description,
                "assign_to": todo_id.assign_to,
                "due_date":todo_id.due_date,
            }
            return valid_response(data,pagination_info=None, status=200)
        except Exception as e:
            return invalid_response(str(e), status=400)

    @http.route("/v1/todo_update/<int:todo_record>",methods=["PUT"],type="http",auth="none",csrf=False)
    def update_todo_api(self,todo_record):
       try:
            todo_record=request.env['todo.task'].sudo().search([('id','=',todo_record)])
            if not todo_record:
                return invalid_response("This ID not found", status=404)

            args=request.httprequest.data.decode()
            vals=json.loads(args)
            todo_record.write(vals)

            data = {
                "id": todo_record.id,
                "task_name": todo_record.task_name,
                "description": todo_record.description,
                "assign_to": todo_record.assign_to.id if todo_record.assign_to else None,
                "status": todo_record.status,
                "due_date": todo_record.due_date
            }
            return valid_response(data,pagination_info=None, status=200)

       except Exception as e:
           return invalid_response(str(e), status=400)

    @http.route("/v1/todo_delete/<int:todo_id>",methods=["DELETE"],type="http",auth="none",csrf=False)
    def delete_todo_api(self,todo_id):
        try:
            todo_id=request.env['todo.task'].sudo().search([('id','=',todo_id)])
            if not todo_id:
                return invalid_response("This ID not found", status=404)

            todo_id.unlink()
            return valid_response(None,None,status=200)
        except Exception as e:
            return invalid_response(str(e), status=400)


    @http.route("/v1/GetAll_todo",methods=["GET"],type="http",auth="none",csrf=False)
    def get_all_todo_api(self):
        try:
            # get data from request
            params=parse_qs(request.httprequest.query_string.decode('utf-8'))
            todo_domain=[]

            page=offset=None
            limit=3

            if params.get('page'):
                page=int(params.get('page')[0])
            if params.get('limit'):
                limit=int(params.get('limit')[0])
            if page:
                offset=(page*limit)-limit

            # filteration on return records
            if params.get('status'):
                todo_domain +=[('status','=',params.get('status')[0])]

            record_ids=request.env['todo.task'].sudo().search(todo_domain,offset=offset,limit=limit,order='id desc')
             # count records using search_count
            record_counts=request.env['todo.task'].sudo().search_count(todo_domain)
            if not record_ids:
                return invalid_response("This Ids not found", status=404)
            data =[]
            for record_id in record_ids:
                data.append({
                    "id": record_id.id,
                    "task_name": record_id.task_name,
                    "description": record_id.description,
                    "assign_to": record_id.assign_to.id if record_id.assign_to else None,
                    "status": record_id.status,
                    "due_date": record_id.due_date
                })
                # pagination as metadata
            pagination_info={
                "total": record_counts,
                "page": page if page else 1,
                "limit": limit,
                "pages":math.ceil(record_counts/limit) if limit else 1,
            }

            return valid_response(data,pagination_info, status=200)

        except Exception as e:
            return invalid_response(str(e), status=400)
