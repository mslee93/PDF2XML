import os
import sys
import re
#import time
import xml.etree.ElementTree as xml
# from miner_text_generator import extract_text_by_page
from xml.dom import minidom
import io
from pdfminer3.converter import TextConverter
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfpage import PDFPage
from pdfminer3.converter import XMLConverter
# from uuid import uuid4

# exe_path = r'"C:\Program Files (x86)\ABBYY FineReader 12/FineCMD.exe"'
# input_folder_path = os.path.join(os.getcwd(), 'ocr', 'Input_Temp')
# output_folder_path = os.path.join(os.getcwd(), 'ocr', 'Output_Temp')


class FolderControl(object):
    abbyy_path = r'"C:\Program Files (x86)\ABBYY FineReader 12/FineCMD.exe"'
    input_folder_path = "C:\\api\\ocr\\Input_Temp"
    output_folder_path = "C:\\api\\ocr\\Output_Temp"
    # input_folder_path = str(os.path.join(os.getcwd(), 'api', 'ocr', 'Input_Temp'))
    # output_folder_path = str(os.path.join(os.getcwd(), 'api', 'ocr', 'Output_Temp'))
	
    '''
    @staticmethod
    def deleteOldFiles(days=1):
        now = time.time()
        for folder in [FolderControl.input_folder_path, FolderControl.output_folder_path]:
            for filename in os.listdir(folder):
                if os.path.getmtime(os.path.join(folder, filename)) < now - days * 86400:
                    if os.path.isfile(os.path.join(folder, filename)):
                        os.remove(os.path.join(folder, filename))
    '''

class File(object):
    def __init__(self, job_id, file_name, file_data):
        self.job_id = job_id
        self.temp_file_name = str(job_id) + os.path.splitext(os.path.basename(file_name))[-1]
        # self.temp_file_name = str(uuid4()) + os.path.splitext(os.path.basename(file_name))[-1]
        self.file_data = file_data
        self.input_file_path = None
        self.__saveInputFile()
        # FolderControl.deleteOldFiles()

    def __saveInputFile(self):
        input_file_path = str(os.path.join(FolderControl.input_folder_path, self.temp_file_name))
        with open(input_file_path, 'wb') as f:
            f.write(self.file_data)

        self.input_file_path = input_file_path

    def deleteInputFile(self):
        if self.input_file_path is not None:
            if os.path.exists(self.input_file_path):
                os.remove(self.input_file_path)
                self.input_file_path = None


class OCR(File):
    def __init__(self, job_id, file_name, file_data, lang, extension):
        super(OCR, self).__init__(job_id, file_name, file_data)
        self.lang = lang
        self.extension = extension
        self.output_file_path = None

    def run(self):
        temp_output_file_path = str(os.path.join(FolderControl.output_folder_path,
                                                 os.path.splitext(os.path.basename(self.temp_file_name))[0]+'.'+self.extension))
        os.system(FolderControl.abbyy_path+' '+self.input_file_path+' /lang '+self.lang+' /out '+temp_output_file_path+' /quit')
        # output_file_path = os.path.join(FolderControl.output_folder_path, self.file_name)
        # os.rename(temp_output_file_path, output_file_path)
        self.output_file_path = temp_output_file_path
        super(OCR, self).deleteInputFile()

    def deleteOutputFile(self):
        if self.output_file_path is not None:
            if os.path.exists(self.output_file_path):
                os.remove(self.output_file_path)
                self.output_file_path = None

    def result(self):
        with open(self.output_file_path, "rb") as f:
            b = f.read()
        self.deleteOutputFile()

        return b


class XML(OCR):
    def __init__(self, job_id, file_name, file_data, lang, extension, xml_type):
        super(XML, self).__init__(job_id, file_name, file_data, lang, extension)
        self.output_xml_content = None
        self.xml_type = xml_type

    def run(self):
        super(XML, self).run()
        if self.xml_type == 'letter':
            resource_manager = PDFResourceManager()
            fake_file_handle = io.BytesIO()
            converter = XMLConverter(resource_manager, fake_file_handle)
            page_interpreter = PDFPageInterpreter(resource_manager, converter)

            with open(self.output_file_path, 'rb') as fh:

                for page in PDFPage.get_pages(fh,
                                              caching=True,
                                              check_extractable=True):
                    page_interpreter.process_page(page)

                text = fake_file_handle.getvalue().decode('utf-8')
                text += '\n</pages>'
                self.output_xml_content = text

            # close open handles
            converter.close()
            fake_file_handle.close()
            super(XML, self).deleteOutputFile()
        else:
            def __extract_text_by_page(pdf_path):
                with open(pdf_path, 'rb') as fh:
                    for page in PDFPage.get_pages(fh,
                                                  caching=True,
                                                  check_extractable=True):
                        resource_manager = PDFResourceManager()
                        fake_file_handle = io.StringIO()
                        converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8')
                        page_interpreter = PDFPageInterpreter(resource_manager, converter)
                        page_interpreter.process_page(page)

                        text = fake_file_handle.getvalue()
                        # text = text.encode('utf-8')
                        yield text

                        # close open handles
                        converter.close()
                        fake_file_handle.close()

            def __replace_nontext(text, replacement=u'\uFFFD'):
                _char_tail = ''
                if sys.maxunicode > 0x10000:
                    _char_tail = u'%s-%s' % (chr(0x10000), chr(min(sys.maxunicode, 0x10FFFF)))
                _nontext_sub = re.compile(r'[^\x09\x0A\x0D\x20-\uD7FF\uE000-\uFFFD%s]' % _char_tail, re.U).sub

                return _nontext_sub(replacement, text)

            root = xml.Element('{filename}'.format(filename='Result'))
            pages = xml.Element('Pages')
            root.append(pages)
            counter = 1

            for page in __extract_text_by_page(self.output_file_path):
                text = xml.SubElement(pages, 'Page_{}'.format(counter))
                text.text = page[:]
                counter += 1
            
            #root.append(pages)
            tree = xml.ElementTree(root)
            #xml_string = xml.tostring(tree, 'utf-8', method='xml')
            xml_string = xml.tostring(root, 'utf-8', method='xml')
            xml_string = __replace_nontext(xml_string.decode('utf-8'), replacement=u'\uFFFD').encode('utf-8')
            #xml_string += '\n</pages>'
            parsed_string = minidom.parseString(xml_string)
            pretty_string = parsed_string.toprettyxml(indent='  ')
            
            #pretty_string += '\n</pages>'
            # with open(output_file_path, 'w', encoding="utf-8") as f:
            #     f.write(pretty_string)

            self.output_xml_content = pretty_string
            super(XML, self).deleteOutputFile()

    def result(self):
        return self.output_xml_content

