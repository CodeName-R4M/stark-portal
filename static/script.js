// Vulnerable: JWT secret exposed in client-side code
const JWT_SECRET = "stark_industries_super_secret_key_2024";

console.log("=== Stark Industries JWT System ===");
console.log("Debug: JWT System Initialized");
console.log("Security Note: JWT operations use key - " + JWT_SECRET);
console.log("===================================");

// Helper function to decode JWT tokens
function decodeJWT(token) {
    try {
        const parts = token.split('.');
        if (parts.length !== 3) {
            throw new Error('Invalid JWT token');
        }
        
        const header = JSON.parse(atob(parts[0]));
        const payload = JSON.parse(atob(parts[1]));
        
        return {
            header: header,
            payload: payload,
            signature: parts[2]
        };
    } catch (error) {
        console.error('Error decoding JWT:', error);
        return null;
    }
}

// Function to create a fake admin JWT (for educational purposes)
function createAdminJWT() {
    console.warn("Security Vulnerability: Creating admin JWT with exposed secret!");
    
    const payload = {
        username: 'admin',
        role: 'admin',
        exp: Math.floor(Date.now() / 1000) + (60 * 60) // 1 hour expiry
    };
    
    // In a real scenario, this would be done server-side
    // This demonstrates the vulnerability of exposed secrets
    console.log("Admin JWT created with payload:", payload);
    console.log("Using secret:", JWT_SECRET);
    
    // Note: Actual JWT creation requires proper libraries
    // This is just for demonstration
    return "fake.admin.jwt.token";
}

// Cookie helper function
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Display current JWT token info
function displayTokenInfo() {
    const token = getCookie('auth_token');
    if (token) {
        const decoded = decodeJWT(token);
        if (decoded) {
            console.log("Current JWT Token:", decoded);
            console.log("User Role:", decoded.payload.role);
        }
    } else {
        console.log("No JWT token found");
    }
}

// Auto-display token info on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log("Page loaded - JWT system active");
    displayTokenInfo();
    
    // Security vulnerability demonstration
    console.log("💀 SECURITY WARNING: JWT Secret is exposed in client-side code!");
    console.log("💀 Attackers can forge JWT tokens using: " + JWT_SECRET);
});