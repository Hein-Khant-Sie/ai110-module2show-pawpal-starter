# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
I used the classes Pet, CareTask, PetOwner, DailyPlan, and Scheduler. The Pet class stores basic information like name, species, and age. The CareTask class represents tasks such as feeding or walking, including details like duration, priority, category, and whether it is required. The PetOwner class manages the owner’s information, preferences, and list of pets. The DailyPlan class holds the tasks and reasons for a specific day. The Scheduler class is responsible for organizing and sorting tasks, for example by priority.

Each class has a clear role: Pet and CareTask store data, while PetOwner, DailyPlan, and Scheduler handle organization and management.


**b. Design changes**
Overall, the skeleton matches the intended roles well, and I do not see a missing core relationship in the current model. The main risks are consistency and future validation rather than class wiring.

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**
One tradeoff in my scheduler is that conflict detection only checks whether tasks have the exact same scheduled time. This keeps the algorithm simple and readable, but it does not detect overlaps based on duration. For example, a task at 10:00 for 30 minutes and another at 10:15 would not be treated as a conflict. I kept this simpler version because it is easier to understand and maintain for this project.

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
