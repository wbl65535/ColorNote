# Tasks: ColorNote - 全栈便利贴应�?

**Input**: Design documents from `/specs/001-colornote-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Include E2E and API tests as required by constitution and plan.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Flask app**: `app/` at repository root for backend code
- **Frontend**: `app/templates/index.html`, `app/static/js/app.js`, `app/static/css/custom.css`
- **Tests**: `tests/api/`, `tests/e2e/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create Flask application structure per implementation plan
- [x] T002 Initialize Python project with Flask 3.0 and SQLAlchemy dependencies
- [x] T003 [P] Configure environment variable management with python-dotenv
- [x] T004 [P] Setup project configuration management in app/config.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Setup TiDB database connection and SQLAlchemy configuration
- [x] T006 Create Note data model in app/models.py per data-model.md specification
- [x] T007 Implement NoteRepository in app/repositories.py for data access layer
- [x] T008 Setup Flask application factory pattern in app/__init__.py
- [x] T009 Create base HTML template in app/templates/index.html with Vue.js and Tailwind CSS
- [x] T010 Configure Vercel Blob integration for image storage
- [x] T011 Setup error handling and response formatting in Flask app
- [x] T012 Create test configuration and fixtures in tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 创建新笔�?(Priority: P1) 🎯 MVP

**Goal**: Allow users to create new notes with title and content through a sliding panel interface

**Independent Test**: Can create notes and see them appear in the list without any other features

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T013 [P] [US1] API contract test for POST /api/notes in tests/api/test_notes_api.py
- [x] T014 [P] [US1] E2E test for note creation flow in tests/e2e/test_note_creation.py

### Implementation for User Story 1

- [x] T015 [US1] Implement POST /api/notes endpoint in app/routes.py for note creation
- [x] T016 [US1] Add Vue.js sliding panel component in app/static/js/app.js for note creation UI
- [x] T017 [US1] Implement form validation for title (�?0 chars) and content (�?00 chars)
- [x] T018 [US1] Add color selection with 6 predefined colors in the creation panel
- [x] T019 [US1] Connect frontend form to API endpoint with proper error handling
- [x] T020 [US1] Update note list display to show newly created notes immediately
- [x] T021 [US1] Add responsive design for mobile vertical screen layout

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - 查看笔记列表 (Priority: P1)

**Goal**: Display all notes in chronological order with preview content and responsive mobile layout

**Independent Test**: Can view the list of created notes with proper formatting and interactions

### Tests for User Story 2 ⚠️

- [x] T022 [P] [US2] API contract test for GET /api/notes in tests/api/test_notes_api.py
- [x] T023 [P] [US2] E2E test for notes list display in tests/e2e/test_notes_list.py

### Implementation for User Story 2

- [x] T024 [US2] Implement GET /api/notes endpoint returning notes in descending creation order
- [x] T025 [US2] Create Vue.js note card components with title, content preview, and color background
- [x] T026 [US2] Implement content truncation for notes (3 lines max on mobile viewport)
- [x] T027 [US2] Add click handler to note cards for opening edit panel (UI only, no edit logic yet)
- [x] T028 [US2] Setup proper spacing and responsive grid layout for note cards
- [x] T029 [US2] Add empty state display when no notes exist
- [x] T030 [US2] Implement smooth scrolling and performance optimization for large note lists

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - 编辑现有笔记 (Priority: P2)

**Goal**: Allow users to modify existing notes including title, content, and color through the same interface

**Independent Test**: Can edit any existing note and see changes reflected immediately

### Tests for User Story 3 ⚠️

- [x] T031 [P] [US3] API contract test for PUT /api/notes/<id> in tests/api/test_notes_api.py
- [x] T032 [P] [US3] E2E test for note editing flow in tests/e2e/test_note_editing.py

### Implementation for User Story 3

- [x] T033 [US3] Implement PUT /api/notes/<id> endpoint for updating existing notes
- [x] T034 [US3] Connect note card clicks to populate edit panel with existing data
- [x] T035 [US3] Implement form pre-population with current note title, content, and color
- [x] T036 [US3] Add visual feedback for color selection in edit panel
- [x] T037 [US3] Update API call to handle both create and update operations
- [x] T038 [US3] Refresh note list display after successful edits
- [x] T039 [US3] Add form validation and error handling for edit operations

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - 删除笔记 (Priority: P2)

**Goal**: Allow users to delete notes with confirmation dialog and proper cleanup

**Independent Test**: Can delete notes with confirmation and see them removed from the list

### Tests for User Story 4 ⚠️

- [x] T040 [P] [US4] API contract test for DELETE /api/notes/<id> in tests/api/test_notes_api.py
- [x] T041 [P] [US4] E2E test for note deletion flow in tests/e2e/test_note_deletion.py

### Implementation for User Story 4

- [x] T042 [US4] Implement DELETE /api/notes/<id> endpoint for note deletion
- [x] T043 [US4] Add delete button to edit panel with proper positioning
- [x] T044 [US4] Implement confirmation dialog with "Cancel" and "Delete" options
- [x] T045 [US4] Add visual styling for delete button (red color, clear icon)
- [x] T046 [US4] Handle confirmation dialog animations and overlay
- [x] T047 [US4] Remove note from list display after successful deletion
- [x] T048 [US4] Add error handling for deletion failures

**Checkpoint**: At this point, User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - 颜色主题选择 (Priority: P3)

**Goal**: Provide 6 predefined color themes for notes with visual selection feedback

**Independent Test**: Can select different colors and see proper visual feedback during creation/editing

### Tests for User Story 5 ⚠️

- [x] T049 [P] [US5] E2E test for color selection UI in tests/e2e/test_color_selection.py

### Implementation for User Story 5

- [x] T050 [US5] Implement 6 predefined color options in edit panel UI
- [x] T051 [US5] Add visual indicators for color selection (borders, checkmarks)
- [x] T052 [US5] Update panel background color in real-time when selecting colors
- [x] T053 [US5] Ensure color buttons meet minimum touch target size (44px)
- [x] T054 [US5] Add hover and focus states for accessibility
- [x] T055 [US5] Test color selection across all note operations (create/edit)

**Checkpoint**: At this point, User Stories 1-5 should all work independently

---

## Phase 8: User Story 6 - 图片上传与展�?(Priority: P3)

**Goal**: Allow users to upload and display images in notes with Vercel Blob storage

**Independent Test**: Can upload images to notes and see them displayed properly

### Tests for User Story 6 ⚠️

- [x] T056 [P] [US6] API contract test for image upload endpoints in tests/api/test_image_upload.py
- [x] T057 [P] [US6] E2E test for image upload and display in tests/e2e/test_image_upload.py

### Implementation for User Story 6

- [x] T058 [US6] Implement Vercel Blob integration in app/services.py for image upload
- [x] T059 [US6] Add image upload UI to edit panel with file picker
- [x] T060 [US6] Implement image preview in edit panel (max 200px width, maintain aspect ratio)
- [x] T061 [US6] Add image validation (file type, size limit 5MB, max 3 images per note)
- [x] T062 [US6] Update API endpoints to handle multipart form data with images
- [x] T063 [US6] Store image URLs in database and upload files to Vercel Blob
- [x] T064 [US6] Display first image thumbnail in note list cards
- [x] T065 [US6] Implement image deletion functionality with confirmation
- [x] T066 [US6] Add loading states and error handling for image operations
- [x] T067 [US6] Ensure images display properly in both list and edit views

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T068 [P] Add comprehensive error handling and user-friendly error messages
- [x] T069 [P] Implement loading states and skeleton screens for better UX
- [x] T070 [P] Add accessibility features (ARIA labels, keyboard navigation)
- [x] T071 [P] Optimize mobile performance and touch interactions
- [x] T072 [P] Add data persistence validation and recovery mechanisms
- [x] T073 [P] Implement comprehensive logging for debugging and monitoring
- [x] T074 [P] Add environment-specific configuration management
- [x] T075 [P] Create deployment configuration for Vercel production
- [x] T076 [P] Add performance monitoring and metrics collection
- [x] T077 [P] Final security review and input sanitization
- [x] T078 [P] Documentation updates and README completion

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 �?P2 �?P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but independently testable
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- API endpoints before frontend integration
- Core functionality before visual polish
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- Within each story, API and UI tasks can often be parallelized

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "API contract test for POST /api/notes in tests/api/test_notes_api.py"
Task: "E2E test for note creation flow in tests/e2e/test_note_creation.py"

# Launch implementation tasks in parallel:
Task: "Implement POST /api/notes endpoint in app/routes.py"
Task: "Add Vue.js sliding panel component in app/static/js/app.js"
Task: "Implement form validation for title and content"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Note Creation)
4. Complete Phase 4: User Story 2 (Notes List)
5. **STOP and VALIDATE**: Test the core CRUD operations work independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational �?Foundation ready
2. Add User Story 1 �?Test independently �?Deploy/Demo (Basic note creation)
3. Add User Story 2 �?Test independently �?Deploy/Demo (Notes list display)
4. Add User Stories 3-4 �?Test independently �?Deploy/Demo (Full CRUD)
5. Add User Stories 5-6 �?Test independently �?Deploy/Demo (Enhanced features)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Stories 1 & 2 (Core CRUD - P1)
   - Developer B: User Stories 3 & 4 (Enhanced CRUD - P2)
   - Developer C: User Stories 5 & 6 (Advanced features - P3)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
