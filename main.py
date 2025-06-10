import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import pytz 
import csv



def get_api_data():
    job_list_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Engineer%20&location=United%20States&position=1&pageNum=0&start=125'

    print(job_list_url)
    response = requests.get(job_list_url)
    
    list_data = response.text
    
    list_soup = BeautifulSoup(list_data, 'html.parser')
    page_soup = list_soup.find_all('li')
    
    print(page_soup)
    
    
    job_id_list = []
    for job in page_soup:
        base_card_div = job.find("div",{"class":"base-card"})
        job_id = base_card_div.get('data-entity-urn').split(":")[3]
        job_id_list.append(job_id)    
    
    job_list = []
    for job_id in job_id_list:
    # job_id = '4115022421'
        job_description_url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
        response_job_description = requests.get(job_description_url)
        job_description_data = response_job_description.text
        job_description_data_soup = BeautifulSoup(job_description_data, 'html.parser')

        job_post = {}
        job_post['job_id'] = job_id 
        try:
            job_post['job_title'] = job_description_data_soup.find('h2',{"class":'top-card-layout__title font-sans text-lg papabear:text-xl font-bold leading-open text-color-text mb-0 topcard__title'}).text.strip()
        except:
            job_post['job_title'] = None
        try:
            job_post['company_name'] = job_description_data_soup.find('a',{"class":'topcard__org-name-link topcard__flavor--black-link'}).text.strip()
        except:
            job_post['company_name'] = None
        try:
            job_post['descprition'] = job_description_data_soup.find('div',{"class":'show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden'})
        except:
            job_post['descprition'] = None
        job_list.append(job_post)
        
        


    # def clean_html(text):
    #     """Remove HTML tags and extra spaces from the job description."""
    #     if text is None:
    #         return ""
    #     print(text)
    #     soup = BeautifulSoup(text, "html.parser")
    #     clean_text = soup.get_text(" ")  # Get text with spaces
    #     clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # Remove excessive whitespace
    #     return clean_text


    def clean_html(text):
        """Remove HTML tags and extra spaces from the job description."""
        if text is None:
            return ""
        print(type(text))
        print(f"Processing text: {text[:100]}...")  # Print a snippet for debugging

        soup = BeautifulSoup(text, "html.parser")
        print(f"Soup object type: {type(soup)}")  # Check if BeautifulSoup is initialized correctly

        clean_text = soup.get_text(" ")  # Extract text
        print(f"Extracted text: {clean_text[:100]}...")  # Debugging

        clean_text = re.sub(r'\s+', ' ', clean_text).strip()  # Remove excessive spaces
        return clean_text

#     text = """
#      <div class="show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden">
#             Position Description<br/><br/>CGI is seeking a motivated individual who is passionate about helping the team and clients achieve excellence. Qualified candidates will have a creative, holistic, and systematic approach to problem-solving.<br/><br/>The Data Engineer is responsible for assisting our client with building a robust data infrastructure to extract insights that enable data driven decision making. The successful candidate will have a broad understanding of computer and information science principles to build data pipelines using SQL, Python and PySpark. They will import and sync to various data sources, clean and standardize data elements, and fix data quality issues. They will collect, manage, and convert raw data into a usable format for the data scientists<br/><br/>This position is located in our Arlington, VA office; however, a hybrid working model is acceptable for candidates within the National Capital Region.<br/><br/>Due to the nature of work a Secret Security Clearance is required.<br/><br/>Your future duties and responsibilities<br/><br/>Creating and maintaining scalable data pipelines from multiple sources<br/><br/><ul><li> Collecting and storing data from multiple sources</li><li> Building, maintaining, and optimizing data tables</li><li> Coordinating with data scientists to ensure data infrastructure needs are met</li><li> Communicating with leadership to articulate progress of ongoing data initiatives as well as any blockers.</li><li> Building and maintaining processes to monitor and ensure data quality ensuring accurate information is fed into executive level dashboards<br/><br/></li></ul>Required qualifications to be successful in this role:<br/><br/><strong>Required Qualifications To Be Successful In This Role<br/><br/></strong>Bachelor's Degree in similar field.<br/><br/>2-3 years of experience in data integration and management<br/><br/><ul><li> Experience with SQL, Python and PySpark</li><li> Excellent analytical and problem-solving skill</li><li> Excellent oral and written communication skills<br/><br/></li></ul>Desired qualifications/non-essential skills required:<br/><br/><ul><li> Experience with Databricks or Data Lakes desired<br/><br/></li></ul>CGI is required by law in some jurisdictions to include a reasonable estimate of the compensation range for this role. The determination of this range includes various factors not limited to skill set, level, experience, relevant training, and licensure and certifications. To support the ability to reward for merit-based performance, CGI typically does not hire individuals at or near the top of the range for their role. Compensation decisions are dependent on the facts and circumstances of each case. A reasonable estimate of the current range for this role in the U.S. is $85,000.00 - $121,900.00.<br/><br/>CGI Federal's benefits are offered to eligible professionals on their first day of employment to include:<br/><br/><ul><li> Competitive compensation</li><li> Comprehensive insurance options</li><li> Matching contributions through the 401(k) plan and the share purchase plan</li><li> Paid time off for vacation, holidays, and sick time</li><li> Paid parental leave</li><li> Learning opportunities and tuition assistance</li><li> Wellness and Well-being programs<br/><br/></li></ul>#CGIFederalJob<br/><br/><strong>Together, as owners, let’s turn meaningful insights into action.<br/><br/></strong>Life at CGI is rooted in ownership, teamwork, respect and belonging. Here, you’ll reach your full potential because…<br/><br/>You are invited to be an owner from day 1 as we work together to bring our Dream to life. That’s why we call ourselves CGI Partners rather than employees. We benefit from our collective success and actively shape our company’s strategy and direction.<br/><br/>Your work creates value. You’ll develop innovative solutions and build relationships with teammates and clients while accessing global capabilities to scale your ideas, embrace new opportunities, and benefit from expansive industry and technology expertise.<br/><br/>You’ll shape your career by joining a company built to grow and last. You’ll be supported by leaders who care about your health and well-being and provide you with opportunities to deepen your skills and broaden your horizons.<br/><br/>Come join our team—one of the largest IT and business consulting services firms in the world.<br/><br/>Qualified applicants will receive consideration for employment without regard to their race, ethnicity, ancestry, color, sex, religion, creed, age, national origin, citizenship status, disability, pregnancy, medical condition, military and veteran status, marital status, sexual orientation or perceived sexual orientation, gender, gender identity, and gender expression, familial status or responsibilities, reproductive health decisions, political affiliation, genetic information, height, weight, or any other legally protected status or characteristics.<br/><br/>CGI provides reasonable accommodations to qualified individuals with disabilities. If you need an accommodation to apply for a job in the U.S., please email the CGI U.S. Employment Compliance mailbox at US_Employment_Compliance@cgi.com. You will need to reference the Position ID of the position in which you are interested. Your message will be routed to the appropriate recruiter who will assist you. <strong>Please note, this email address is only to be used for those individuals who need an accommodation to apply for a job. Emails for any other reason or those that do not include a Position ID will not be returned.<br/><br/></strong>We make it easy to translate military experience and skills! Click here to be directed to our site that is dedicated to veterans and transitioning service members.<br/><br/>All CGI offers of employment in the U.S. are contingent upon the ability to successfully complete a background investigation. Background investigation components can vary dependent upon specific assignment and/or level of US government security clearance held. Dependent upon role and/or federal government security clearance requirements, and in accordance with applicable laws, some background investigations may include a credit check. CGI will consider for employment qualified applicants with arrests and conviction records in accordance with all local regulations and ordinances.<br/><br/>CGI will not discharge or in any other manner discriminate against employees or applicants because they have inquired about, discussed, or disclosed their own pay or the pay of another employee or applicant. However, employees who have access to the compensation information of other employees or applicants as a part of their essential job functions cannot disclose the pay of other employees or applicants to individuals who do not otherwise have access to compensation information, unless the disclosure is (a) in response to a formal complaint or charge, (b) in furtherance of an investigation, proceeding, hearing, or action, including an investigation conducted by the employer, or (c) consistent with CGI’s legal duty to furnish information.<br/><br/>
#   </div>
#     """
#     clean_html(text)
    # Process job descriptions
    for job in job_list:
        print(job["descprition"])
        job["descprition"] = clean_html(str(job["descprition"]))

    df = pd.DataFrame(job_list)
    
    new_df = pd.read_csv(' final_df.csv' )
    new_df = pd.concat([new_df, df], ignore_index=True)

    # Save back to CSV
    new_df.to_csv('cleaned_jobs.csv', index=False)
    # Save to CSV
    # csv_filename = "cleaned_jobs.csv"
    # with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    #     writer = csv.DictWriter(file, fieldnames=["job_id", "job_title", "company_name", "descprition"])
    #     writer.writeheader()
    #     writer.writerows(job_list)

    # print(f"Cleaned job data saved to {csv_filename}")


if __name__=="__main__":
    get_api_data()
      
    # scraping_data(url)