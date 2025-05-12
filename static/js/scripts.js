function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.remove('opacity-0');
    
    setTimeout(() => {
        toast.classList.add('opacity-0');
    }, 6000);
}


// function showToast(message, type = "info") {
//     const toast = document.getElementById("toast");
//     if (!toast) return;

//     toast.textContent = message;

//     // Set color based on type
//     toast.classList.remove("bg-primary", "bg-green-500", "bg-yellow-500", "bg-red-500");

//     if (type === "success") toast.classList.add("bg-green-500");
//     else if (type === "warning") toast.classList.add("bg-yellow-500");
//     else if (type === "error") toast.classList.add("bg-red-500");
//     else toast.classList.add("bg-primary");

//     // Show toast
//     toast.classList.remove("opacity-0");
//     toast.classList.add("opacity-100");

//     // Auto-hide after 4 seconds
//     setTimeout(() => {
//         toast.classList.remove("opacity-100");
//         toast.classList.add("opacity-0");
//     }, 6000);
// }