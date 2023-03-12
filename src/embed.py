import base64
import os
import tempfile
from embedded import *

class EmbeddedResource:

    __resources = {
        "unr-256x256.ico":UNR_256X256_ICO,
        "MyriadPro-Light.ttf":MYRIADPRO_LIGHT_TTF,
    }

    def __init__(self, resource: str):
        if resource in self.__resources.keys():
            self.resource = resource
        else:
            raise Exception("Resource Not Found")

    def __enter__(self) -> tempfile:
        self.tmp = tempfile.NamedTemporaryFile(suffix=os.path.splitext(self.resource)[1], delete=False)
        self.tmp.close()

        with open(self.tmp.name, "wb") as file:
            data = base64.b64decode(self.__resources.get(self.resource))
            file.write(data)

        return self.tmp.name

    def __exit__(self, et, ev, etb):
        return True
    
    @staticmethod
    def embed_resources(resources):
        resource_dict, resource_lines = EmbeddedResource.__get_embedded_resources()

        new_embeds = []
        
        try:
            for to_embed in resources:
                
                to_embed_path = os.path.abspath(to_embed)
                to_embed = os.path.basename(to_embed_path)

                if not os.path.isfile(to_embed_path):
                    raise Exception("Unable to embed {to_embed_path}. Resource does not exist.")

                resource_key = EmbeddedResource.__sanitize_resource_key(to_embed)

                line = ""
                if resource_dict.get(resource_key) != None:
                    line = resource_lines[resource_dict.get(resource_key)]
                    line = EmbeddedResource.__replace_resource_line_with_new_resource(line, to_embed_path)
                    resource_lines[resource_dict.get(resource_key)] = line

                else:
                    line = EmbeddedResource.__write_new_resource_line(resource_key, to_embed_path)
                    resource_lines.append(line)
                    new_embeds.append(to_embed)

            EmbeddedResource.__write_embedded_resource_file(resource_lines)
            EmbeddedResource.__update_embedded_resources(new_embeds)
            
        except Exception as e:
            print(e)
            EmbeddedResource.clear_resources()

    @staticmethod
    def clear_resources():
        EmbeddedResource.__clear_embedded_file()
        EmbeddedResource.__clear_embedded_resources()

    @staticmethod
    def __get_embedded_resources():
        embedded = EmbeddedResource.__get_embedded_resource_file()

        resource_dict = {}
        resource_lines = []

        with open(embedded, "r") as embedded_resources:
            lines = embedded_resources.readlines()
            for i, line in enumerate(lines):
                resource_key = line[:line.find("=")]
                resource_dict.update({resource_key:i})
            resource_lines = lines

        return resource_dict, resource_lines
    
    @staticmethod
    def __sanitize_resource_key(to_embed):
        return to_embed.replace("-", "_").replace(".", "_").upper()
    
    @staticmethod
    def __encode_resource_to_str(to_embed_path, as_python_str=False):
        with open(to_embed_path, "rb") as file:
            data = file.read()
            encoded_data = base64.b64encode(data).decode()
            return f"\"{encoded_data}\"" if as_python_str else encoded_data
        
    @staticmethod
    def __write_new_resource_line(resource_key, to_embed_path):
        return f"{resource_key}={EmbeddedResource.__encode_resource_to_str(to_embed_path, as_python_str=True)}\n"
    
    @staticmethod
    def __replace_resource_line_with_new_resource(line, to_embed_path):
        line = EmbeddedResource.__clear_resource_line(line)
        line += f"{EmbeddedResource.__encode_resource_to_str(to_embed_path, as_python_str=True)}\n"
        return line
    
    @staticmethod
    def __clear_resource_line(line):
        return line[:line.find('=') + 1]
    
    @staticmethod
    def __get_embedded_resource_file():
        return os.path.realpath(os.path.dirname(os.path.abspath(__file__))+"/embedded.py")
    
    @staticmethod
    def __write_embedded_resource_file(resource_lines):
        embedded = EmbeddedResource.__get_embedded_resource_file()
        with open(embedded, "w") as target:
            target.write("".join(resource_lines))
    
    @staticmethod
    def __clear_embedded_file():
        embedded = EmbeddedResource.__get_embedded_resource_file()
        with open(embedded, "w") as target:
            pass
    
    @staticmethod
    def __update_embedded_resources(new_embeds):
        if len(new_embeds) > 0:
            insert_index = -1
            this_file_as_lines = []
            with open(os.path.abspath(__file__), 'r') as this:
                in_resource_dict = False
                this_file_as_lines = this.readlines()
                for i, line in enumerate(this_file_as_lines):
                    if ("__resources" + " = {") in line:
                        in_resource_dict = True
                    if "}" in line and in_resource_dict:
                        insert_index = i
                        in_resource_dict = False

            for new_resource in new_embeds:
                resource_key = EmbeddedResource.__sanitize_resource_key(new_resource)
                this_file_as_lines.insert(insert_index, f"{8*' '}\"{new_resource}\":{resource_key},\n")

            with open(os.path.abspath(__file__), 'w') as this:
                this.write("".join(this_file_as_lines))
    
    @staticmethod
    def __clear_embedded_resources():
        start_index = -1
        end_index = -1
        this_file_as_lines = []
        with open(os.path.abspath(__file__), 'r') as this:
            in_resource_dict = False
            this_file_as_lines = this.readlines()
            for i, line in enumerate(this_file_as_lines):
                if ("__resources" + " = {") in line:
                    start_index = i + 1
                    in_resource_dict = True

                if "}" in line and in_resource_dict:
                    end_index = i
                    in_resource_dict = False
        
        for _ in range(start_index, end_index):
            print(this_file_as_lines.pop(start_index))

        with open(os.path.abspath(__file__), 'w') as this:
            this.write("".join(this_file_as_lines))