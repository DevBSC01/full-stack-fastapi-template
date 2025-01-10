## Data model for a CV App

### Tables / Fields

- CV
  - ID
  - Name
  - Created at
  - Edited at
  - Recipient

- Job
  - ID
  - Position
  - Company
  - Location
  - Start
  - End

- Task
  - ID
  - Name
  - Description
  - Duration

- Skill
  - ID
  - Name
  - Rating

- School
  - ID
  - School
  - Subject
  - Degree
  - Location
  - Start
  - End

- Contact
  - ID
  - First name
  - Last name
  - Address
  - ZIP code
  - Location
  - Phone
  - Email
  - Birthdate
  - Photo
  - Marital status

- Knowledge
  - ID
  - Name
  - Description
  - Rating

- Languages
  - ID
  - Language
  - Level

- Certificates
  - ID
  - Name
  - Description
  - Date

### Relations

- Job ---1:N--- Task
- Task --1:N--- Skill
- CV ---1:N--- Job
- CV ---1:N--- School
- CV ---1:1--- Contact