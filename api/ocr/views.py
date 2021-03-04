from .ocr import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest


@csrf_exempt
def OCR_API(request, _type):

    def __invalid(status, message):
        _response = HttpResponseBadRequest('')
        _response['status'] = status
        _response['message'] = message
        return _response

    if request.method == 'POST':
        data = request.POST.copy()
        job_id = data.get('job_id')
        # file_name = data.get('file_name')
        # file_content = data.get('file_content')
        lang = data.get('lang')
        file_data = request.FILES['file'].read()
        file_name = request.FILES['file'].name.replace('"', '')
        # print(request.FILES['file'].content_type)

        if file_data and file_name:
            if _type == 'ocr':
                extension = data.get('extension')
                if job_id and lang and extension:
                    try:
                        task = OCR(job_id, file_name, file_data, lang, extension)
                        task.run()
                        response = HttpResponse(task.result(), content_type='application/'+extension)
                        response['Content-Disposition'] = 'attachment; filename="' + job_id + '.' + extension + '"'
                        response['status'] = '000'
                        response['message'] = 'Done'

                        return response
                    except:
                        return __invalid('100', 'OCR Engine Error')
                else:
                    return __invalid('001', 'Input Error')
            elif _type == 'xml':
                xml_type = data.get('xml_type')
                if xml_type is None:
                    xml_type = 'page'
                if job_id and lang:
                    try:
                        task = XML(job_id, file_name, file_data, lang, 'pdf', xml_type)
                        task.run()
                        response = HttpResponse(task.result(), content_type='application/xml')
                        response['Content-Disposition'] = 'attachment; filename="' + job_id + '.xml' + '"'
                        response['status'] = '000'
                        response['message'] = 'Done'

                        return response
                    except:
                        return __invalid('100', 'XML Engine Error')
                else:
                    return __invalid('001', 'Input Error')
            else:
                return __invalid('300', 'Invalid URL')
        else:
            return __invalid('010', 'No File')
    else:
        return __invalid('500', 'Invalid Request')
