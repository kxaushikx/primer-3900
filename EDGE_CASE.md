# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
- pre-existing student in the same course. must throw error
- the same thing as above, but in the update stage, should not be allowed to place a same name same class situation.
2) How you have accounted for this in your implementation
- ccorss checked db data to check if there is a duplicate, if yes, then return error.