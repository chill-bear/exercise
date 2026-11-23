Requirements
Implement a working URL shortener: given a long URL, produce a short code; given the short code, resolve the original URL. It must actually run end-to-end (CLI or a small API/back end).
Discuss and handle the key design points the interviewer drills into:
Input validation — reject malformed URLs; handle oversized URLs.
Encoding scheme — e.g. hashing (md5) vs. counter/base62; how to handle hash collisions.
Storage of the short→long mapping — an in-memory hashmap is usually accepted for this scope (Redis / a real DB are typically deemed overkill); persist by serializing to a JSON file and reloading on startup.
Capacity estimation — estimate memory for N URLs and discuss partitioning/sharding if it grows.
Write unit tests; a 90%+ line/branch coverage bar is commonly stated. Cover invalid input, collisions, duplicate requests for the same URL, and very long URLs.
Notes
Framing varies: some interviewers present it as a from-scratch coding task, others as a "design a URL-shortening API" round where you define endpoints and request/response formats — the same core problem with more or less design emphasis. One MLE candidate was rejected specifically for a weak design answer here, so treat the design discussion as load-bearing.
Production follow-up: how would this look in production? Expected directions include storing the mapping in a database rather than memory, and deploying the service (e.g. containerized on Kubernetes).
AI tools are allowed; after generating code, refactor for naming, comments, and reusability, then run a few real URLs through it.
Preparation
Write a minimal shortener yourself (base62 over an incrementing id, plus a hashmap and JSON persistence) so you can defend the encoding and storage choices without the AI.
Prepare crisp answers for collision handling, capacity/memory math for N URLs, and the in-memory-vs-DB and deploy-to-prod follow-ups.
Build a small test suite covering invalid input, duplicate URLs, collisions, and oversized input, and be ready to show coverage.

Q:
Part 1 — Algorithm and Data Structures
1. Explain how Base62 encoding works. Why use Base62 instead of a random string?
2. What is the time complexity of shortening and resolving a URL?
3. How do you guarantee unique short codes?
4. What happens if two URLs generate the same short code?
5. How would you handle integer ID overflow?
Part 2 — Storage and Scalability
6. Why did you choose a hashmap?
7. How much memory would you need to store 1 million URLs? What about 100 million?
8. What happens if the JSON file becomes too large?
9. How would you replace the in-memory storage with a database?
10. How would you prevent duplicate short codes when multiple servers are running concurrently?
Part 3 — Testing
11. How would you systematically test this application?
12. What edge cases should be covered?
13. How would you test collision handling?
14. How would you verify that persistence works after restarting the application?
15. How would you measure and demonstrate test coverage?
Part 4 — Production Readiness
16. How would you deploy this service to production using Docker and Kubernetes?
17. What happens when multiple users shorten URLs simultaneously?
18. How would you implement rate limiting?
19. What monitoring and logging would you add?
20. What changes would you make before submitting this code for production review?