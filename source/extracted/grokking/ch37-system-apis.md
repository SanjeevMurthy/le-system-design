# 5. System APIs

> Source: System Design - Grokking (Notes), Chapter 37, Pages 9-9

## Key Concepts

- 3. Some Design Considerations
Pastebin shares some requirements with URL Shortening service, but there are some additional design
considerations we should keep in mind.
What should be the limit on the

## Content

3. Some Design Considerations
Pastebin shares some requirements with URL Shortening service, but there are some additional design
considerations we should keep in mind.
What should be the limit on the amount of text user can paste at a time?  We can limit users
not to have Pastes bigger than 10MB to stop the abuse of the service.
Should we impose size limits on custom URLs?  Since our service supports custom URLs, users
can pick any URL that they like, but providing a custom URL is not mandatory. However, it is
reasonable (and often desirable) to impose a size limit on custom URLs, so that we have a consistent
URL database.
4. Capacity Estimation and Constraints
Our services will be read-heavy; there will be more read requests compared to new Pastes creation. We
can assume a 5:1 ratio between read and write.
Traffic estimates: Pastebin services are not expected to have traffic similar to Twitter or Facebook,
let’s assume here that we get one million new pastes added to our system every day. This leaves us with
five million reads per day.
New Pastes per second:
1M / (24 hours * 3600 seconds) ~= 12 pastes/sec
Paste reads per second:
5M / (24 hours * 3600 seconds) ~= 58 reads/sec
Storage estimates: Users can upload maximum 10MB of data; commonly Pastebin like services are
used to share source code, configs or logs. Such texts are not huge, so let’s assume that each paste on
average contains 10KB.
At this rate, we will be storing 10GB of data per day.
1M * 10KB => 10 GB/day
If we want to store this data for ten years we would need the total storage capacity of 36TB.
With 1M pastes every day we will have 3.6 billion Pastes in 10 years. We need to generate and store
keys to uniquely identify these pastes. If we use base64 encoding ([A-Z, a-z, 0-9, ., -]) we would need
six letters strings:
64^6 ~= 68.7 billion unique strings
If it takes one byte to store one character, total size required to store 3.6B keys would be:
3.6B * 6 => 22 GB
22GB is negligible compared to 36TB. To keep some margin, we will assume a 70% capacity model
(
i
d
’
h
% f
l
i
i
)
hi h
i
(meaning we don’t want to use more than 70% of our total storage capacity at any point), which raises
our storage needs to 51.4TB.
Bandwidth estimates: For write requests, we expect 12 new pastes per second, resulting in 120KB of
ingress per second.
12 * 10KB => 120 KB/s
As for the read request, we expect 58 requests per second. Therefore, total data egress (sent to users)
will be 0.6 MB/s.
58 * 10KB => 0.6 MB/s
Although total ingress and egress are not big, we should keep these numbers in mind while designing
our service.
Memory estimates: We can cache some of the hot pastes that are frequently accessed. Following the
80-20 rule, meaning 20% of hot pastes generate 80% of traffic, we would like to cache these 20%
pastes
Since we have 5M read requests per day, to cache 20% of these requests, we would need:
0.2 * 5M * 10KB ~= 10 GB
5. System APIs
We can have SOAP or REST APIs to expose the functionality of our service. Following could be the
definitions of the APIs to create/retrieve/delete Pastes:
addPaste(api_dev_key, paste_data, custom_url=None user_name=None, paste_name=None,
 expire_date=None)
Parameters:
api_dev_key (string): The API developer key of a registered account. This will be used to, among other
things, throttle users based on their allocated quota.
paste_data (string): Textual data of the paste.
custom_url (string): Optional custom URL.
user_name (string): Optional user name to be used to generate URL.
paste_name (string): Optional name of the paste
expire_date (string): Optional expiration date for the paste.
Returns: (string)
A successful insertion returns the URL through which the paste can be accessed, otherwise, it will
return an error code.
Similarly, we can have retrieve and delete Paste APIs:
getPaste(api_dev_key, api_paste_key)
Wh
“
i
k
” i
i
i
h P
K
f h
b
i
d Thi API
ill

