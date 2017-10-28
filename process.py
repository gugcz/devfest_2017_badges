# -*- coding: utf-8 -*-
import csv


def normalize(v):
    return v.replace("-", "")


def image(v):
    table = str.maketrans("áčďéěíňóřšťúůýžÁČĎÉĚÍŇÓŘŠŤÚŮÝŽ",
                          "acdeeinorstuuyzACDEEINORSTUUYZ")
    return "img/{}.png".format(
        v.replace(' ', '_').replace(',', '')
            .replace('.', '').lower().translate(table))


def main():
    result = []
    images = set()
    with open('sample_data_from_tito.csv', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for r in reader:
            # from headers
            # odict_keys(
            #     ['Number', 'Ticket Created Date', 'Ticket Last Updated Date',
            #      'Ticket', 'Ticket Full Name', 'Ticket First Name',
            #      'Ticket Last Name', 'Ticket Email', 'Ticket Company Name',
            #      'Ticket Phone Number', 'Event', 'Void Status', 'Price',
            #      'Discount Status', 'Ticket Reference', 'Tags',
            #      'Unique Ticket URL', 'Unique Order URL', 'Order Reference',
            #      'Order Name', 'Order Email', 'Order Company Name',
            #      'Order Phone Number', 'Order Discount Code', 'Order IP',
            #      'Order Created Date', 'Order Completed Date',
            #      'Payment Reference', 'Company/Organization', 'Job Title',
            #      'Where do you live?', 'Do you have any dietary restrictions?',
            #      'Gender', 'Interests', 'Twitter nickname', 'Conference'])

            # result headers
            # "Type,Name,Company,Company Logo,Job Title,Interest 1,Interest 2,Interest 3,Twitter"

            interests = list(map(lambda x: x.strip(),
                                 r["Interests"].split(',')))
            t = ""
            if r["Ticket"].startswith("Partner ticket"):
                t = "Partner"
            if r["Ticket"].startswith("Speaker ticket"):
                t = "Speaker"
            if r["Ticket"].startswith("ORG ticket"):
                t = "Organizer"

            company = normalize(r["Company/Organization"])
            company_logo = ""
            if r["Ticket"].startswith("Company-funded") or \
                    r["Ticket"].startswith("Partner ticket"):
                company_logo = company
                company = ""
                if not company_logo:
                    company_logo = normalize(r["Ticket Company Name"])
                company_logo = image(company_logo)
                images.add(company_logo)

            ticket = {
                "Type": t,
                "Name": normalize(r["Ticket Full Name"]),
                "Company": company,
                "Company Logo": company_logo,
                "Job Title": normalize(r["Job Title"]),
                "Interest 1": normalize(interests[0] if len(interests) > 0
                                        else ""),
                "Interest 2": normalize(interests[1] if len(interests) > 1
                                        else ""),
                "Interest 3": normalize(interests[2] if len(interests) > 2
                                        else ""),
                "Twitter": normalize(r["Twitter nickname"]),
            }

            # print(ticket)
            result.append(ticket)

    with open('out.csv', 'w', encoding="utf-8") as f:
        dw = csv.DictWriter(f, fieldnames=result[0].keys())
        dw.writeheader()
        dw.writerows(result)

    with open("logos.txt", "w") as f:
        for i in images:
            f.write(i + '\n')


if __name__ == "__main__":
    main()
