# :robot: Scouts Training Bot
A script written in Python with Selenium to log in to the scouts training website and automatically complete all training modules, watch all videos, open all required documents, and take all tests.

<div align="center">
    <img src="https://img.shields.io/github/last-commit/aiden2480/scouts-training-bot?color=yellow" alt="Last commit" />
    <img src="https://img.shields.io/github/license/aiden2480/scouts-training-bot" alt="Licence" />
    <img src="https://img.shields.io/github/languages/code-size/aiden2480/scouts-training-bot" alt="Code size" />
</div>

## :key: Setup
The program will run the training curriculum that is currently selected. To change this, login and scroll to the bottom of the index page, then click `Set as My Training` under the desired curriculum.

Ensure you have Google Chrome installed before running. Run the following commands to install requirements and run the script. If you don't have Python installed, you can [download the latest release](https://github.com/aiden2480/scouts-training-bot/releases/latest) instead.

```
$ pip install -r requirements.txt
$ python main.py
```

You can also optionally add a `.env` file in the root directory, or next to the executable to provide credentials to login with, rather than having to manually sign into the browser. 

| Property   | Description                                |
|------------|--------------------------------------------|
| `branch`   | The two or three letter code of the branch |
| `username` | Your username for Scouts Training          |
| `password` | Your password for Scouts Training          |

## :outbox_tray: Sample output
```
[MODULE] Enqueuing emodule 'Camp Equipment'
[MODULE] Enqueuing emodule 'Being Safe with Trailers'
[MODULE] Enqueuing emodule 'Camp Catering'
[MODULE] Enqueuing emodule 'Hygiene and Health'
[MODULE] Enqueuing emodule 'Safety at Camp'
[MODULE] Marking video 'Jamboree Highlights' complete
[MODULE] Enqueuing emodule 'Understanding Major Events'
[MODULE] Enqueuing emodule 'Camp Life at Major Events'
[MODULE] Marking emodule 'Exploring Unit Camping' as complete
[MODULE] Marking emodule 'Location and Logistics' as complete
[MODULE] Marking emodule 'Staffing and Communication' as complete
[MODULE] Marking emodule 'Camp Budgeting' as complete
[MODULE] Marking emodule 'Planning the Camp Program' as complete
[MODULE] Marking emodule 'Scouts Australia Environment Charter' as complete
[MODULE] Marking emodule 'Camp Life' as complete
[MODULE] Marking emodule 'Construction Projects' as complete
[MODULE] Marking emodule 'Camp Equipment' as complete
[MODULE] Marking emodule 'Being Safe with Trailers' as complete
[MODULE] Marking emodule 'Camp Catering' as complete
[MODULE] Marking emodule 'Hygiene and Health' as complete
[MODULE] Marking emodule 'Safety at Camp' as complete
[MODULE] Marking emodule 'Understanding Major Events' as complete
[MODULE] Marking emodule 'Camp Life at Major Events' as complete
[MODULE] No post-module exam required

[MODULE] Traversing module 'Growing Scouting'
[MODULE] Skipping completed object 'Meet the G Team'
[MODULE] Skipping completed object 'Scout Hall or Draculas Castle'
[MODULE] Skipping completed object 'How to be Inviting'
[MODULE] Skipping completed object 'How to be Welcoming'
[MODULE] Skipping completed object 'External Relationships'
[MODULE] Skipping completed object 'Collaborative, Not Competitive'
[MODULE] Skipping completed object "It's about the Vibe"
[MODULE] Skipping completed object 'Communication - Getting it Wrong'
[MODULE] Skipping completed object 'Communication - Getting it Right'
[MODULE] Skipping completed object 'Promote your Success'
[MODULE] Skipping completed object 'Time to Recruit'
[MODULE] Skipping completed object 'Go Active on Recruiting Adults'
[MODULE] Skipping completed object 'Including New Members'
[MODULE] Skipping completed object 'Video - Youth Engagement'
[MODULE] Marking video 'The Power of the Program' complete
[MODULE] Marking video 'Good Programs, Good Memories, Good PR' complete
[MODULE] Marking video 'Once a Scout, Always a Scout' complete
[MODULE] Marking video 'Recognition - Getting it Wrong' complete
[MODULE] Marking video 'Awards and Appreciation' complete
[MODULE] Marking document 'The Key to Retention in Scouting (COVID-19 Edition)' complete
[MODULE] Marking video 'Signing off from the G Team' complete
[MODULE] Marking document 'Take a walk around' complete
[MODULE] No post-module exam required

[MODULE] Traversing module 'Plan>Do>Review>'
[MODULE] Skipping completed object 'Scouts'
[MODULE] Skipping completed object 'Venturer Scouts'
[MODULE] Skipping completed object 'Rover Scouts'
[MODULE] Opening post-module exam
[EXAM] 3/5 exam questions correct
[EXAM] 5/9 exam questions correct
[EXAM] 8/14 exam questions correct
[EXAM] 9/17 exam questions correct
[EXAM] 10/19 exam questions correct
[EXAM] Exam pass mark achieved

[MODULE] Traversing module 'Youth Led Programming'
[MODULE] Skipping completed object 'Games - Leading Games'
[MODULE] Skipping completed object 'Games - Creativity Challenge'
[MODULE] Skipping completed object 'Youth Led Programming - Benefits'
[MODULE] Opening post-module exam
[EXAM] 0/5 exam questions correct
[EXAM] 1/8 exam questions correct
[EXAM] 2/11 exam questions correct
[EXAM] 4/12 exam questions correct
[EXAM] 6/13 exam questions correct
[EXAM] Exam pass mark achieved

[MODULE] Traversing module 'Being Inclusive'
[MODULE] Skipping completed object "Harry Smith's Story"
[MODULE] Skipping completed object "Let's Talk about Mental Health"
[MODULE] Skipping completed object 'Including New Members'
[MODULE] Opening post-module exam
[EXAM] 1/5 exam questions correct
[EXAM] 3/9 exam questions correct
[EXAM] 4/10 exam questions correct
[EXAM] 7/12 exam questions correct
[EXAM] Exam pass mark achieved

[MODULE] Traversing module 'Managing Behaviours'
[MODULE] Skipping completed object 'Cyberbullying'
[MODULE] Skipping completed object 'Breaking the Cycle'
[MODULE] Skipping completed object 'Dealing with Bullying'
[MODULE] Opening post-module exam
[EXAM] 0/5 exam questions correct
[EXAM] 3/8 exam questions correct
[EXAM] 4/12 exam questions correct
[EXAM] 5/13 exam questions correct
[EXAM] 6/15 exam questions correct
[EXAM] 7/16 exam questions correct
[EXAM] Exam pass mark achieved
```
