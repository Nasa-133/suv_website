document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.getElementById("heroCarousel");

    if (carousel) {
        // Bootstrap carousel event nomi to'g'ri - "slid.bs.carousel" emas, "slide.bs.carousel"
        carousel.addEventListener("slide.bs.carousel", function () {
            // AOS mavjudligini tekshirish
            if (typeof AOS !== 'undefined') {
                AOS.refresh();
            }
        });

        // Carousel tugagandan keyin ham AOS refresh qilish
        carousel.addEventListener("slid.bs.carousel", function () {
            if (typeof AOS !== 'undefined') {
                AOS.refresh();
            }
        });
    }

    // Animatsiyani pauzaga tushirish (hover)
    const carouselItems = document.querySelectorAll(".carousel-item");

    carouselItems.forEach(item => {
        item.addEventListener("mouseenter", () => {
            const animatedElements = document.querySelectorAll(".water-drop, .ripple");
            animatedElements.forEach(el => {
                if (el.style.animationPlayState !== undefined) {
                    el.style.animationPlayState = "paused";
                }
            });
        });

        item.addEventListener("mouseleave", () => {
            const animatedElements = document.querySelectorAll(".water-drop, .ripple");
            animatedElements.forEach(el => {
                if (el.style.animationPlayState !== undefined) {
                    el.style.animationPlayState = "running";
                }
            });
        });
    });

    // Video autoplay muted (error handling bilan)
    const videos = document.querySelectorAll("video");
    videos.forEach(video => {
        if (video && typeof video.play === 'function') {
            video.muted = true; // Autoplay uchun muted bo'lishi kerak
            video.play().catch(error => {
                console.log("Video autoplay blocked:", error);
            });
        }
    });

    // Mahsulot buyurtma tugmalari uchun event listener
    const orderButtons = document.querySelectorAll('.order-btn');
    orderButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const productName = this.dataset.productName;
            const productPrice = this.dataset.productPrice;

            // Modal ochish (agar orderModal mavjud bo'lsa)
            const orderModal = document.getElementById('orderModal');
            if (orderModal) {
                // Modal ichidagi inputlarga ma'lumotlarni to'ldirish
                const productNameInput = orderModal.querySelector('input[name="product_name"]');
                const productPriceInput = orderModal.querySelector('input[name="product_price"]');

                if (productNameInput) productNameInput.value = productName;
                if (productPriceInput) productPriceInput.value = productPrice;

                // Bootstrap modal ochish
                const modal = new bootstrap.Modal(orderModal);
                modal.show();
            }
        });
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Lazy loading uchun Intersection Observer
    const images = document.querySelectorAll('img[data-src]');
    if (images.length > 0) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    }

    // Performance optimization: prefetch uchun
    const prefetchLinks = document.querySelectorAll('a[data-prefetch]');
    prefetchLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            const url = this.href;
            if (url && !document.querySelector(`link[href="${url}"]`)) {
                const prefetchLink = document.createElement('link');
                prefetchLink.rel = 'prefetch';
                prefetchLink.href = url;
                document.head.appendChild(prefetchLink);
            }
        });
    });
});