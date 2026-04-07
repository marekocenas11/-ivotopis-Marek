// Životopis Marek - JavaScript
document.addEventListener('DOMContentLoaded', function () {

    // Karty: kliknutím na nadpis rozbalit/sbalit obsah
    var cards = document.querySelectorAll('.card');

    cards.forEach(function (card) {
        var heading = card.querySelector('h2');
        var content = card.querySelector('.card-content');

        if (!heading || !content) return;

        // Na začátku vše otevřít
        content.classList.add('open');

        heading.setAttribute('title', 'Klikněte pro sbalení/rozbalení');

        heading.addEventListener('click', function () {
            content.classList.toggle('open');
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
