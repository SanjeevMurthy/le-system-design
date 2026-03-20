# �� You should always clarify requirements at the beginning of the interview. Be

> Source: System Design - Grokking (Notes), Chapter 67, Pages 16-16

## Key Concepts

- Designing Dropbox
Let's design a file hosting service like Dropbox or Google Drive. Cloud file storage enables users to store
their data on remote servers. Usually, these servers are maintained by clo

## Content

Designing Dropbox
Let's design a file hosting service like Dropbox or Google Drive. Cloud file storage enables users to store
their data on remote servers. Usually, these servers are maintained by cloud storage providers and made
available to users over a network (typically through the Internet). Users pay for their cloud data storage on a
monthly basis.
Similar Services: OneDrive, Google Drive
Difficulty Level: Medium
1. Why Cloud Storage?
#
Cloud file storage services have become very popular recently as they simplify the storage and
exchange of digital resources among multiple devices. The shift from using single personal computers
to using multiple devices with different platforms and operating systems such as smartphones and
tablets each with portable access from various geographical locations at any time, is believed to be
accountable for the huge popularity of cloud storage services. Following are some of the top benefits of
such services:
Availability: The motto of cloud storage services is to have data availability anywhere, anytime. Users
can access their files/photos from any device whenever and wherever they like.
Reliability and Durability: Another benefit of cloud storage is that it offers 100% reliability and
durability of data. Cloud storage ensures that users will never lose their data by keeping multiple
copies of the data stored on different geographically located servers.
Scalability: Users will never have to worry about getting out of storage space. With cloud storage you
have unlimited storage as long as you are ready to pay for it.
If you haven’t used dropbox.com before, we would highly recommend creating an account there and
uploading/editing a file and also going through the different options their service offers. This will help
you a lot in understanding this chapter.
2. Requirements and Goals of the System
#
�� You should always clarify requirements at the beginning of the interview. Be
sure to ask questions to find the exact scope of the system that the interviewer has in
mind.
What do we wish to achieve from a Cloud Storage system? Here are the top-level requirements for our
system:

