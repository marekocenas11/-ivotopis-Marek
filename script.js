// Životopis Marek - JavaScript
document.addEventListener('DOMContentLoaded', function () {

    var profileImage = document.getElementById('profileImage');
    var imageModal = document.getElementById('imageModal');
    var imageModalClose = document.getElementById('imageModalClose');

    if (profileImage && imageModal && imageModalClose) {
        profileImage.addEventListener('click', function () {
            imageModal.classList.add('open');
            imageModal.setAttribute('aria-hidden', 'false');
        });

        imageModalClose.addEventListener('click', function () {
            imageModal.classList.remove('open');
            imageModal.setAttribute('aria-hidden', 'true');
        });

        imageModal.addEventListener('click', function (event) {
            if (event.target === imageModal) {
                imageModal.classList.remove('open');
                imageModal.setAttribute('aria-hidden', 'true');
            }
        });
    }

    function setOpenHeight(content) {
        content.style.maxHeight = content.scrollHeight + 'px';
    }

    // Karty: kliknutím na nadpis rozbalit/sbalit obsah
    var cards = document.querySelectorAll('.card');

    cards.forEach(function (card) {
        var heading = card.querySelector('h2');
        var content = card.querySelector('.card-content');

        if (!heading || !content) return;

        // Na začátku vše otevřít
        content.classList.add('open');
        setOpenHeight(content);

        heading.setAttribute('title', 'Klikněte pro sbalení/rozbalení');

        heading.addEventListener('click', function () {
            if (content.classList.contains('open')) {
                content.classList.remove('open');
                content.style.maxHeight = '0px';
                return;
            }

            content.classList.add('open');
            setOpenHeight(content);
        });
    });

    window.addEventListener('resize', function () {
        cards.forEach(function (card) {
            var content = card.querySelector('.card-content');
            if (content && content.classList.contains('open')) {
                setOpenHeight(content);
            }
        });
    });

    // Plynulé scrollování při kliknutí na navigaci
    var navLinks = document.querySelectorAll('.navbar a');

    navLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            var targetId = this.getAttribute('href');
            if (targetId.startsWith('#')) {
                e.preventDefault();
                var target = document.querySelector(targetId);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

    // Zvýraznění aktivní sekce v navigaci při scrollování
    window.addEventListener('scroll', function () {
        var scrollPos = window.scrollY + 120;

        navLinks.forEach(function (link) {
            var targetId = link.getAttribute('href');
            if (!targetId.startsWith('#')) return;
            var section = document.querySelector(targetId);
            if (!section) return;

            if (section.offsetTop <= scrollPos && section.offsetTop + section.offsetHeight > scrollPos) {
                link.style.background = '#1a237e';
                link.style.color = '#fff';
            } else {
                link.style.background = '';
                link.style.color = '';
            }
        });
    });

    console.log('Životopis načten.');
});
