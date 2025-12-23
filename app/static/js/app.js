// ColorNote Vue.js Application
const { createApp, ref, onMounted, computed } = Vue;

// Color options for notes
const AVAILABLE_COLORS = [
    { value: '#FFE57F', name: 'Yellow' },
    { value: '#FFB3BA', name: 'Pink' },
    { value: '#BAE1FF', name: 'Blue' },
    { value: '#BAFFC9', name: 'Green' },
    { value: '#E0BBE4', name: 'Purple' },
    { value: '#FFDAC1', name: 'Orange' }
];

// API base URL
const API_BASE = window.location.origin + '/api';

// Vue App
const app = createApp({
    setup() {
        // Reactive data
        const notes = ref([]);
        const loading = ref(true);
        const isPanelOpen = ref(false);
        const showDeleteConfirm = ref(false);
        const currentNote = ref({
            id: null,
            title: '',
            content: '',
            color: '#FFE57F',
            image_urls: []
        });
        const isEditing = ref(false);

        // Computed properties
        const isValidNote = computed(() => {
            return currentNote.value.title.trim().length > 0 &&
                   currentNote.value.content.trim().length > 0 &&
                   currentNote.value.title.length <= 30 &&
                   currentNote.value.content.length <= 500;
        });

        // Methods
        const loadNotes = async () => {
            try {
                const response = await fetch(`${API_BASE}/notes`);
                if (!response.ok) throw new Error('Failed to load notes');
                const data = await response.json();
                notes.value = data.notes;
            } catch (error) {
                console.error('Error loading notes:', error);
                // For demo purposes, continue with empty notes
                notes.value = [];
            } finally {
                loading.value = false;
            }
        };

        const showCreatePanel = () => {
            currentNote.value = {
                id: null,
                title: '',
                content: '',
                color: '#FFE57F',
                image_urls: []
            };
            isEditing.value = false;
            isPanelOpen.value = true;
        };

        const editNote = (note) => {
            currentNote.value = {
                id: note.id,
                title: note.title,
                content: note.content,
                color: note.color,
                image_urls: [...(note.image_urls || [])]
            };
            isEditing.value = true;
            isPanelOpen.value = true;
        };

        const closePanel = () => {
            isPanelOpen.value = false;
            currentNote.value = {
                id: null,
                title: '',
                content: '',
                color: '#FFE57F',
                image_urls: []
            };
        };

        const saveNote = async () => {
            if (!isValidNote.value) return;

            try {
                const formData = new FormData();
                formData.append('title', currentNote.value.title.trim());
                formData.append('content', currentNote.value.content.trim());
                formData.append('color', currentNote.value.color);

                // Handle images if any
                if (currentNote.value.newImages && currentNote.value.newImages.length > 0) {
                    currentNote.value.newImages.forEach((file, index) => {
                        formData.append('images', file);
                    });
                }

                const url = isEditing.value
                    ? `${API_BASE}/notes/${currentNote.value.id}`
                    : `${API_BASE}/notes`;

                const method = isEditing.value ? 'PUT' : 'POST';

                const response = await fetch(url, {
                    method: method,
                    body: formData
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Failed to save note');
                }

                const savedNote = await response.json();

                if (isEditing.value) {
                    // Update existing note in the list
                    const index = notes.value.findIndex(n => n.id === savedNote.id);
                    if (index !== -1) {
                        notes.value[index] = savedNote;
                    }
                } else {
                    // Add new note to the beginning of the list
                    notes.value.unshift(savedNote);
                }

                closePanel();

            } catch (error) {
                console.error('Error saving note:', error);
                alert(`保存失败: ${error.message}`);
            }
        };

        const deleteNote = () => {
            if (isEditing.value && currentNote.value.id) {
                showDeleteConfirm.value = true;
            }
        };

        const confirmDelete = async () => {
            if (!currentNote.value.id) return;

            try {
                const response = await fetch(`${API_BASE}/notes/${currentNote.value.id}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Failed to delete note');
                }

                // Remove note from the list
                notes.value = notes.value.filter(n => n.id !== currentNote.value.id);

                showDeleteConfirm.value = false;
                closePanel();

            } catch (error) {
                console.error('Error deleting note:', error);
                alert(`删除失败: ${error.message}`);
            }
        };

        const cancelDelete = () => {
            showDeleteConfirm.value = false;
        };

        const selectColor = (color) => {
            currentNote.value.color = color;
        };

        const triggerFileInput = () => {
            const fileInput = document.getElementById('file-input');
            if (fileInput) {
                fileInput.click();
            }
        };

        const handleFileUpload = (event) => {
            const files = Array.from(event.target.files);
            const maxImages = 3 - currentNote.value.image_urls.length;

            if (files.length > maxImages) {
                alert(`最多只能添加 ${maxImages} 张图片`);
                return;
            }

            // Validate file types and sizes
            const validFiles = files.filter(file => {
                // Check file type
                if (!file.type.startsWith('image/')) {
                    alert(`${file.name} 不是有效的图片文件`);
                    return false;
                }

                // Check file size (5MB limit)
                if (file.size > 5 * 1024 * 1024) {
                    alert(`${file.name} 文件大小超过5MB限制`);
                    return false;
                }

                return true;
            });

            currentNote.value.newImages = validFiles;
        };

        const removeImage = (index) => {
            currentNote.value.image_urls.splice(index, 1);
        };

        const formatDate = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            const now = new Date();
            const diffTime = Math.abs(now - date);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays === 1) {
                return '今天';
            } else if (diffDays === 2) {
                return '昨天';
            } else if (diffDays <= 7) {
                return `${diffDays - 1}天前`;
            } else {
                return date.toLocaleDateString('zh-CN');
            }
        };

        // Initialize
        onMounted(() => {
            loadNotes();
        });

        return {
            // Data
            notes,
            loading,
            isPanelOpen,
            showDeleteConfirm,
            currentNote,
            isEditing,
            AVAILABLE_COLORS,

            // Computed
            isValidNote,

            // Methods
            showCreatePanel,
            editNote,
            closePanel,
            saveNote,
            deleteNote,
            confirmDelete,
            cancelDelete,
            selectColor,
            triggerFileInput,
            handleFileUpload,
            removeImage,
            formatDate
        };
    }
});

// Mount the app
app.mount('#app');
