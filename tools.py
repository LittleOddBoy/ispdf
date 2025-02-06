import img2pdf
import telebot
import random
import pikepdf
import os
import pdf2docx
from shutil import rmtree
from pdf2docx import parse
import aspose.words as aw
Token = "7566162751:AAF6p67RpMqhDfbBk3NaUeQ9fuN42vVXPbE"

bot = telebot.TeleBot(Token)

def random_name():
    txt = "0123456789"
    name = "".join(random.sample(txt, 9))
    return name

def Chech_User_folder(message):
    print(os.listdir("./Content"))
    if (str(message.chat.id) not in os.listdir("./Content")):
        os.mkdir(f"./Content/{message.chat.id}")

def create_Folder(name, path="./"):
    if name not in os.listdir():
        os.mkdir(f"{path}/{name}")

# list file sorted by Time added
def slistdir(path=None, message=None):
    if message == None:
        directory_path = path
    else:
        directory_path = f"./Content/{message.chat.id}"
    result = []
    

    # Get all files and directories
    entries = os.listdir(directory_path)

    # Sort by creation time (or last metadata change time on some platforms)
    sorted_entries = sorted(
        entries,
        key=lambda entry: os.path.getctime(os.path.join(directory_path, entry))
    )

    # Print sorted entries
    for entry in sorted_entries:
        result.append(f"./{path}/{entry}")
    return result

def Unlock(pdf):
    file = pikepdf.open(pdf)
    file.save(f"{pdf}_Unlocked")
    return file

def Downloadimg(message):

    message = Message_Details(message)

    file_id = message.file_id()
    fileinfo = bot.get_file(file_id)
    image = bot.download_file(fileinfo.file_path)
    with open(file_id, "wb") as imagee:
        imagee.write(image)

def DownloadFile(message):
    message = Message_Details(message)
    file_id = message.file_id()
    fileinfo = bot.get_file(file_id)
    file = bot.download_file(fileinfo.file_path)
    return file

def send_document(message, path):
    with open(path, "rb") as f:
        bot.send_document(message.chat.id, f)

def delete_user_Content(message):
    if str(message.chat.id) in os.listdir("./Content"):
        rmtree(f'./Content/{message.chat.id}')

def saveFile(file, path):
    with open(path, "wb") as f:
        f.write(file)
    return path

# Convert all directory Picturs to PDF
def Convert_imageToPdf(message):
    User_path = f"./Content/{message.chat.id}"
    pdf_path = f"{User_path}.pdf"

    Picturs = slistdir(User_path)

    with open(pdf_path, "wb") as pdf:
        pdf.write(img2pdf.convert(Picturs))

    return pdf_path
    
def imageToPdf(message):
    print(message.text) # For Debug
    if (message.text == back_button):
    
        return "back"
    
    
    elif (message.content_type != "photo"):
        bot.send_message(message.chat.id, "Pleas just Send image ‼️",reply_markup=keyboard)

def get_images(message):
    
    print("a fille recived")
    file = DownloadFile(message)
    path = f"./Content/{message.chat.id}/{random_name()}.jpg"
    saveFile(file, path=path)

def loger(log):
        bot.send_message(1473554980, log)

def message_content_type(message):
    return message.content_type

class Message_Details:
    def __init__(self, message):
        self.message = message
    
    def file_id(self):

        message = self.message.json

        if ("photo" in message):
            return message["photo"][-1]["file_id"]

        elif ("document" in message):
            return message["document"]["file_id"]
        
        else:
            print("content_types not found")
        
    
    def file_path(self):

        message = self.message.json

        if ("photo" in message):
            print (message["photo"])

        elif ("document" in message):
            return message["document"][0]["file_path"]
        
        else:
            print("content_types not found")
def file_extension(file_name = "", extention = ""): # file_name or file_path
    if (file_name.endswith(extention)):
        return True
    else:
        return False

def check_content_type(message, content_type = "", extension = ""):
    if message.content_type == content_type:
        if extension == "":
            return True
        elif (file_extension(message.document.file_name, extension) == True):
            return True
    return False

def convert_pdf_to_docx(message ,pdf_file_path = ""):
    document = aw.Document(pdf_file_path)
    docx_path = f"./Content/{message.chat.id}/{random_name()}.docx"
    document.save(docx_path)
    os.remove(pdf_file_path)
    return docx_path

def is_pdf_file(pdf_path):
    if file_extension(pdf_path, extention=".pdf"):
        try:
            pikepdf.open(pdf_path)
            return True
        except:
            return False
    else:
        return False
def check_file_size(message, size):
    if message.content_type == "document":
        if message.document.file_size <= size:
            return True
        else:
            return False
    elif message.content_type == "photo":
        if message.photo["file_size"] <= size:
            return True
        else:
            return False
        
        
    


        