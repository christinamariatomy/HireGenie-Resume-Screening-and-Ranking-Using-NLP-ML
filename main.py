import csv
import PyPDF2
from flask import Flask, render_template, request
import gcsfs
import pickle
import pandas as pd

app = Flask(__name__, static_url_path='/static', static_folder='static')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/post', methods=['GET', 'POST'])
def index2():
    if request.method == 'POST':
        pdf_file = request.files['pdf_file']
        csv_file = "https://storage.googleapis.com/bucketforhr/empty.csv"

        # Save the uploaded file to a temporary location
        pdf_file_path = "temp/" + pdf_file.filename
        pdf_file.save(pdf_file_path)

        with open(pdf_file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)  # matches this is fine too until here fineeee

            # Write the text to a CSV file using gcsfs
            # fs = gcsfs.GCSFileSystem()  # this is fine toooo
            with open(csv_file, 'a', newline='', encoding='utf-8') as csv_file:  # fineeeee
                writer = csv.writer(csv_file)  # fineeeeee
                for i in range(len(pdf_reader.pages)):  # fineeeeee
                    page = pdf_reader.pages[i]  # fineee
                    text = page.extract_text()  # fineee
                    writer.writerow([text])  # now fine

    return render_template('inner-page.html')



@app.route('/innerpage', methods=['GET', 'POST'])
def innerpage():
    return render_template('inner-page.html')


# path=r'C:\\Users\\AIDEN SAMUEL\\PycharmProjects\\Pythonproject1\lgbm_best.pkl'
# model = pickle.load(open(path, 'rb'))
model1 = pickle.load(open('resume_pipeline.pkl', 'rb'))  # load commm


@app.route('/screen', methods=['GET', 'POST'])
def screen():
    data = pd.read_csv('gs://bucketforhr/cat_14.csv')

    job_categories = ['Advocate', 'Arts', 'Automation Testing', 'Blockchain', 'Business Analyst', 'Civil Engineer',
                      'Data Science', 'Database', 'DevOps Engineer', 'DotNet Developer', 'ETL Developer',
                      'Electrical Engineering', 'HR', 'Hadoop', 'Health and fitness', 'Java Developer',
                      'Mechanical Engineer', 'Network Security Engineer', 'Operations Manager', 'PMO',
                      'Python Developer', 'SAP Developer', 'Sales', 'Testing', 'Web Designing']

    # output1 = model1.predict(data)
    # predicted_categories = [job_categories[i] for i in output1]
    #
    # return f"The job category is predicted as: {predicted_categories}"
    # return render_template('portfolio-details.html')  #html her

    predicted_categories = []
    for index, row in data.iterrows():
        output1 = model1.predict(row)
        predicted_category = job_categories[output1[0]]
        predicted_categories.append(predicted_category)

    return f"The job categories are predicted as /n: {predicted_categories}"

@app.route('/wordc', methods=['GET', 'POST'])
def wordc():
    if request.method == 'POST':
        # pdf_file = request.files['pdf_file']
        #
        # # Save the uploaded file to a temporary location
        # pdf_file_path = "temp/" + pdf_file.filename
        # pdf_file.save(pdf_file_path)

        # Read the PDF file
        pdf_reader = PyPDF2.PdfFileReader(open("C:\Users\AIDEN SAMUEL\PycharmProjects\FlexStart - Copy - Copy\temp\AidenSamuel_Resume.pdf", "rb"))

        # Extract text from PDF pages
        text = ""
        for page in range(pdf_reader.getNumPages()):
            text += pdf_reader.getPage(page).extractText()

        # Generate a WordCloud
        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              min_font_size=10).generate(text)

        # Convert the WordCloud to an image
        image = wordcloud.to_image()

        # Save the image to a temporary location
        image_path = "temp/" + pdf_file.filename + ".png"
        image.save(image_path)

        # Render the image to the user
        return render_template('image.html', image_file=image_path)

    # return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
