# External Fetching Compatibility Guide

## ⚠️ **Important: File Path Changes**

With the implementation of MkDocs, the file structure has been reorganized. **External systems that fetch raw markdown files will need to be updated** to work with the new structure.

## 📁 **File Structure Changes**

### **Before (Original Structure):**
```
ntr-test/
├── overview.md                    # ❌ No longer exists at root
├── vouchers.md                    # ❌ No longer exists at root
├── user-management.md             # ❌ No longer exists at root
├── training-management.md         # ❌ No longer exists at root
├── subscriptions.md               # ❌ No longer exists at root
├── attendance.md                  # ❌ No longer exists at root
├── troubleshooting.md             # ❌ No longer exists at root
├── en/
│   ├── overview.md               # ❌ Moved to docs/en/
│   ├── vouchers.md               # ❌ Moved to docs/en/
│   └── ...
└── sv/
    ├── overview.md               # ❌ Moved to docs/sv/
    ├── vouchers.md               # ❌ Moved to docs/sv/
    └── ...
```

### **After (MkDocs Structure):**
```
ntr-test/
├── docs/                         # ✅ New docs directory
│   ├── en/
│   │   ├── overview.md           # ✅ New location
│   │   ├── vouchers.md           # ✅ New location
│   │   ├── user-management.md    # ✅ New location
│   │   ├── training-management.md # ✅ New location
│   │   ├── subscriptions.md      # ✅ New location
│   │   ├── attendance.md         # ✅ New location
│   │   └── troubleshooting.md    # ✅ New location
│   ├── sv/
│   │   ├── overview.md           # ✅ New location
│   │   ├── vouchers.md           # ✅ New location
│   │   ├── user-management.md    # ✅ New location
│   │   ├── training-management.md # ✅ New location
│   │   ├── subscriptions.md      # ✅ New location
│   │   ├── attendance.md         # ✅ New location
│   │   └── troubleshooting.md    # ✅ New location
│   └── index.md                  # ✅ New homepage
├── mkdocs.yml                    # ✅ MkDocs configuration
└── help-config.json              # ✅ Updated with new paths
```

## 🔧 **Solutions for External Fetching**

### **Option 1: Update External System Paths (Recommended)**

Update your external system to use the new file paths:

#### **Old Paths (No Longer Work):**
```javascript
// ❌ These paths will return 404 errors
const oldPaths = {
  overview: "ntr-test/overview.md",
  vouchers: "ntr-test/vouchers.md",
  userManagement: "ntr-test/user-management.md",
  trainingManagement: "ntr-test/training-management.md",
  subscriptions: "ntr-test/subscriptions.md",
  attendance: "ntr-test/attendance.md",
  troubleshooting: "ntr-test/troubleshooting.md",
  
  // Language-specific paths
  enOverview: "ntr-test/en/overview.md",
  svOverview: "ntr-test/sv/overview.md",
  // ... etc
};
```

#### **New Paths (Updated):**
```javascript
// ✅ Use these new paths
const newPaths = {
  overview: "ntr-test/docs/overview.md",
  vouchers: "ntr-test/docs/vouchers.md",
  userManagement: "ntr-test/docs/user-management.md",
  trainingManagement: "ntr-test/docs/training-management.md",
  subscriptions: "ntr-test/docs/subscriptions.md",
  attendance: "ntr-test/docs/attendance.md",
  troubleshooting: "ntr-test/docs/troubleshooting.md",
  
  // Language-specific paths
  enOverview: "ntr-test/docs/en/overview.md",
  svOverview: "ntr-test/docs/sv/overview.md",
  enVouchers: "ntr-test/docs/en/vouchers.md",
  svVouchers: "ntr-test/docs/sv/vouchers.md",
  // ... etc
};
```

### **Option 2: Use Updated help-config.json**

The `help-config.json` file has been updated to include the new file paths:

```json
{
  "sections": [
    {
      "id": "overview",
      "title": {
        "sv": "Systemöversikt",
        "en": "System Overview"
      },
      "file_paths": {
        "sv": "docs/sv/overview.md",
        "en": "docs/en/overview.md"
      },
      "keywords": ["overview", "system", "features", "architecture"],
      "category": "general"
    }
  ]
}
```

**Use the `file_paths` property** to dynamically fetch the correct files:

```javascript
// ✅ Fetch using updated config
const config = await fetch('ntr-test/help-config.json').then(r => r.json());

config.sections.forEach(section => {
  const svPath = section.file_paths.sv;
  const enPath = section.file_paths.en;
  
  // Fetch Swedish content
  fetch(`ntr-test/${svPath}`).then(r => r.text());
  
  // Fetch English content
  fetch(`ntr-test/${enPath}`).then(r => r.text());
});
```

### **Option 3: Create Backward Compatibility (Advanced)**

If you need to maintain the old paths temporarily, you can create symbolic links or implement a redirect system:

#### **Using Symbolic Links (Windows):**
```powershell
# Create symbolic links to maintain old paths
New-Item -ItemType SymbolicLink -Path "overview.md" -Target "docs/overview.md"
New-Item -ItemType SymbolicLink -Path "en/overview.md" -Target "docs/en/overview.md"
New-Item -ItemType SymbolicLink -Path "sv/overview.md" -Target "docs/sv/overview.md"
```

#### **Using .htaccess (Apache):**
```apache
# Redirect old paths to new paths
RewriteEngine On
RewriteRule ^overview\.md$ docs/overview.md [L]
RewriteRule ^en/overview\.md$ docs/en/overview.md [L]
RewriteRule ^sv/overview\.md$ docs/sv/overview.md [L]
# ... repeat for all files
```

## 📋 **Migration Checklist**

### **For External Systems:**

- [ ] **Update file paths** in your fetching logic
- [ ] **Test all endpoints** to ensure they return content
- [ ] **Update error handling** for 404 responses
- [ ] **Update documentation** for your team
- [ ] **Monitor logs** for any remaining old path requests

### **For Content Management:**

- [ ] **Verify all files** are in the new `docs/` structure
- [ ] **Test MkDocs build** to ensure everything works
- [ ] **Update any scripts** that reference old paths
- [ ] **Communicate changes** to all stakeholders

## 🚨 **Immediate Actions Required**

1. **Identify all external systems** that fetch markdown files
2. **Update the file paths** in those systems
3. **Test the new paths** to ensure they work
4. **Monitor for 404 errors** after deployment
5. **Plan a migration timeline** if needed

## 📞 **Support**

If you need help updating your external systems:

1. **Check the updated `help-config.json`** for correct file paths
2. **Use the new path structure** shown above
3. **Test with a few files first** before updating everything
4. **Contact the development team** if you encounter issues

## ✅ **Benefits of the New Structure**

- **Better organization** with dedicated docs directory
- **MkDocs compatibility** for modern documentation
- **Clearer separation** between source and build files
- **Future-proof structure** for additional features
- **Standard documentation practices** following industry norms

---

**Note:** The old file paths will no longer work after this migration. Please update your external systems as soon as possible to avoid service interruptions.
