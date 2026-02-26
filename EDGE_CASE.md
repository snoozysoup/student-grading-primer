# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
A student's mark could be submitted as a value outside the valid range (e.g. negative or over 100).
2) How you have accounted for this in your implementation
I addressed this by validating that the mark is between 0 and 100 in both the create_student and update_student routes, returning a 404 error if the value is invalid.
