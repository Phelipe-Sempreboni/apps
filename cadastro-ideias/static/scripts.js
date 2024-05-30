document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('save').addEventListener('click', () => {
        alert('Idea saved successfully!');
    });

    document.getElementById('delete').addEventListener('click', () => {
        if (confirm('Are you sure you want to delete this idea?')) {
            alert('Idea deleted successfully!');
        }
    });

    document.getElementById('edit').addEventListener('click', () => {
        alert('Edit mode activated!');
    });

    document.getElementById('view').addEventListener('click', () => {
        alert('Here are all the ideas!');
    });

    document.getElementById('vote').addEventListener('click', () => {
        alert('Thank you for voting!');
    });
});
