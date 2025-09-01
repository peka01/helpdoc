# External Integration Guide

## Overview

This guide explains how to integrate with the Training Management System help documentation using the new multi-app configuration structure. The system now supports multiple applications and locales through a centralized configuration.

## Configuration Structure

### Multi-App Configuration

The `help-config.json` file now uses a multi-app structure that supports:

- **Multiple applications** (ntr-app, future apps)
- **Multiple locales** (sv-se, en-se, future locales)
- **Centralized file path management**
- **Extensible structure** for future growth

### Configuration Schema

```json
{
  "apps": {
    "app-id": {
      "name": "Application Display Name",
      "baseUrl": "path/to/app/docs",
      "locales": {
        "locale-id": {
          "code": "language-code",
          "name": "Language Display Name",
          "file_paths": {
            "section-id": "path/to/section.md"
          }
        }
      }
    }
  },
  "sections": [
    {
      "id": "section-id",
      "title": {
        "sv": "Swedish Title",
        "en": "English Title"
      },
      "keywords": ["keyword1", "keyword2"],
      "category": "category-name"
    }
  ]
}
```

## Current Configuration

### NTR App Configuration

```json
{
  "apps": {
    "ntr-app": {
      "name": "NTR Training Management System",
      "baseUrl": "ntr-test",
      "locales": {
        "sv-se": {
          "code": "sv",
          "name": "Svenska",
          "file_paths": {
            "overview": "docs/sv/overview.md",
            "vouchers": "docs/sv/vouchers.md",
            "user-management": "docs/sv/user-management.md",
            "training-management": "docs/sv/training-management.md",
            "subscriptions": "docs/sv/subscriptions.md",
            "attendance": "docs/sv/attendance.md",
            "troubleshooting": "docs/sv/troubleshooting.md"
          }
        },
        "en-se": {
          "code": "en",
          "name": "English",
          "file_paths": {
            "overview": "docs/en/overview.md",
            "vouchers": "docs/en/vouchers.md",
            "user-management": "docs/en/user-management.md",
            "training-management": "docs/en/training-management.md",
            "subscriptions": "docs/en/subscriptions.md",
            "attendance": "docs/en/attendance.md",
            "troubleshooting": "docs/en/troubleshooting.md"
          }
        }
      }
    }
  }
}
```

## Integration Methods

### Method 1: Direct File Path Access

For simple integrations, you can construct file paths directly:

```javascript
// Base configuration
const APP_ID = 'ntr-app';
const BASE_URL = 'ntr-test';

// Locale and section mapping
const LOCALE_PATHS = {
  'sv-se': 'docs/sv',
  'en-se': 'docs/en'
};

const SECTIONS = {
  'overview': 'overview.md',
  'vouchers': 'vouchers.md',
  'user-management': 'user-management.md',
  'training-management': 'training-management.md',
  'subscriptions': 'subscriptions.md',
  'attendance': 'attendance.md',
  'troubleshooting': 'troubleshooting.md'
};

// Fetch content function
async function fetchContent(locale, section) {
  const localePath = LOCALE_PATHS[locale];
  const sectionFile = SECTIONS[section];
  const filePath = `${BASE_URL}/${localePath}/${sectionFile}`;
  
  try {
    const response = await fetch(filePath);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.text();
  } catch (error) {
    console.error(`Failed to fetch ${filePath}:`, error);
    throw error;
  }
}

// Usage examples
fetchContent('sv-se', 'overview').then(content => {
  console.log('Swedish overview content:', content);
});

fetchContent('en-se', 'troubleshooting').then(content => {
  console.log('English troubleshooting content:', content);
});
```

### Method 2: Dynamic Configuration Loading

For more flexible integrations, load the configuration dynamically:

```javascript
class HelpContentManager {
  constructor(configUrl) {
    this.configUrl = configUrl;
    this.config = null;
  }

  async loadConfig() {
    if (!this.config) {
      const response = await fetch(this.configUrl);
      this.config = await response.json();
    }
    return this.config;
  }

  async fetchContent(appId, locale, sectionId) {
    const config = await this.loadConfig();
    const app = config.apps[appId];
    
    if (!app) {
      throw new Error(`App '${appId}' not found in configuration`);
    }

    const localeConfig = app.locales[locale];
    if (!localeConfig) {
      throw new Error(`Locale '${locale}' not found for app '${appId}'`);
    }

    const filePath = localeConfig.file_paths[sectionId];
    if (!filePath) {
      throw new Error(`Section '${sectionId}' not found for locale '${locale}'`);
    }

    const fullUrl = `${app.baseUrl}/${filePath}`;
    const response = await fetch(fullUrl);
    
    if (!response.ok) {
      throw new Error(`Failed to fetch ${fullUrl}: ${response.status}`);
    }

    return await response.text();
  }

  async getAvailableSections(appId, locale) {
    const config = await this.loadConfig();
    const app = config.apps[appId];
    const localeConfig = app.locales[locale];
    
    return Object.keys(localeConfig.file_paths);
  }

  async getAvailableLocales(appId) {
    const config = await this.loadConfig();
    const app = config.apps[appId];
    
    return Object.keys(app.locales);
  }

  async getAppInfo(appId) {
    const config = await this.loadConfig();
    const app = config.apps[appId];
    
    return {
      name: app.name,
      baseUrl: app.baseUrl,
      locales: Object.keys(app.locales).map(locale => ({
        id: locale,
        code: app.locales[locale].code,
        name: app.locales[locale].name
      }))
    };
  }
}

// Usage
const helpManager = new HelpContentManager('ntr-test/help-config.json');

// Get app information
helpManager.getAppInfo('ntr-app').then(info => {
  console.log('App info:', info);
});

// Get available sections for Swedish
helpManager.getAvailableSections('ntr-app', 'sv-se').then(sections => {
  console.log('Available Swedish sections:', sections);
});

// Fetch specific content
helpManager.fetchContent('ntr-app', 'sv-se', 'overview').then(content => {
  console.log('Swedish overview:', content);
});
```

### Method 3: React Hook (for React applications)

```javascript
import { useState, useEffect } from 'react';

function useHelpContent(configUrl, appId, locale, sectionId) {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchContent() {
      try {
        setLoading(true);
        setError(null);

        // Load configuration
        const configResponse = await fetch(configUrl);
        const config = await configResponse.json();

        // Get file path
        const app = config.apps[appId];
        const localeConfig = app.locales[locale];
        const filePath = localeConfig.file_paths[sectionId];
        const fullUrl = `${app.baseUrl}/${filePath}`;

        // Fetch content
        const contentResponse = await fetch(fullUrl);
        if (!contentResponse.ok) {
          throw new Error(`Failed to fetch content: ${contentResponse.status}`);
        }

        const content = await contentResponse.text();
        setContent(content);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    if (appId && locale && sectionId) {
      fetchContent();
    }
  }, [configUrl, appId, locale, sectionId]);

  return { content, loading, error };
}

// Usage in React component
function HelpContent({ appId, locale, sectionId }) {
  const { content, loading, error } = useHelpContent(
    'ntr-test/help-config.json',
    appId,
    locale,
    sectionId
  );

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!content) return <div>No content available</div>;

  return (
    <div className="help-content">
      <div dangerouslySetInnerHTML={{ __html: marked(content) }} />
    </div>
  );
}
```

## Error Handling

### Common Error Scenarios

1. **App not found**
   ```javascript
   // Error: App 'invalid-app' not found in configuration
   ```

2. **Locale not found**
   ```javascript
   // Error: Locale 'invalid-locale' not found for app 'ntr-app'
   ```

3. **Section not found**
   ```javascript
   // Error: Section 'invalid-section' not found for locale 'sv-se'
   ```

4. **File not found (404)**
   ```javascript
   // Error: Failed to fetch ntr-test/docs/sv/invalid-file.md: 404
   ```

### Recommended Error Handling

```javascript
async function fetchContentWithFallback(appId, locale, sectionId, fallbackLocale = 'en-se') {
  try {
    // Try primary locale
    return await fetchContent(appId, locale, sectionId);
  } catch (error) {
    console.warn(`Failed to fetch ${locale} content:`, error);
    
    // Try fallback locale
    if (locale !== fallbackLocale) {
      try {
        console.log(`Trying fallback locale: ${fallbackLocale}`);
        return await fetchContent(appId, fallbackLocale, sectionId);
      } catch (fallbackError) {
        console.error(`Failed to fetch fallback content:`, fallbackError);
        throw new Error(`Content not available in ${locale} or ${fallbackLocale}`);
      }
    } else {
      throw error;
    }
  }
}
```

## Adding New Applications

To add a new application to the configuration:

1. **Add app configuration** to `help-config.json`:
   ```json
   {
     "apps": {
       "new-app": {
         "name": "New Application",
         "baseUrl": "new-app-docs",
         "locales": {
           "sv-se": {
             "code": "sv",
             "name": "Svenska",
             "file_paths": {
               "section1": "docs/sv/section1.md",
               "section2": "docs/sv/section2.md"
             }
           },
           "en-se": {
             "code": "en",
             "name": "English",
             "file_paths": {
               "section1": "docs/en/section1.md",
               "section2": "docs/en/section2.md"
             }
           }
         }
       }
     }
   }
   ```

2. **Create the documentation structure**:
   ```
   new-app-docs/
   ├── docs/
   │   ├── sv/
   │   │   ├── section1.md
   │   │   └── section2.md
   │   └── en/
   │       ├── section1.md
   │       └── section2.md
   └── help-config.json
   ```

3. **Update integration code** to use the new app ID.

## Best Practices

### 1. **Caching**
Cache the configuration file to avoid repeated requests:
```javascript
const configCache = new Map();

async function getCachedConfig(configUrl) {
  if (!configCache.has(configUrl)) {
    const response = await fetch(configUrl);
    const config = await response.json();
    configCache.set(configUrl, config);
  }
  return configCache.get(configUrl);
}
```

### 2. **Validation**
Validate configuration structure before use:
```javascript
function validateConfig(config) {
  if (!config.apps) {
    throw new Error('Invalid config: missing apps section');
  }
  
  Object.entries(config.apps).forEach(([appId, app]) => {
    if (!app.baseUrl || !app.locales) {
      throw new Error(`Invalid app config for ${appId}`);
    }
  });
}
```

### 3. **TypeScript Support**
For TypeScript projects, define interfaces:
```typescript
interface HelpConfig {
  apps: {
    [appId: string]: {
      name: string;
      baseUrl: string;
      locales: {
        [localeId: string]: {
          code: string;
          name: string;
          file_paths: {
            [sectionId: string]: string;
          };
        };
      };
    };
  };
  sections: Array<{
    id: string;
    title: {
      sv: string;
      en: string;
    };
    keywords: string[];
    category: string;
  }>;
}
```

## Migration from Old Structure

If you're migrating from the old configuration structure:

1. **Update file paths** to use the new `docs/` structure
2. **Replace direct section access** with app-based access
3. **Update locale codes** to use the new format (sv-se, en-se)
4. **Test all integrations** with the new structure

## Support

For integration support:
1. Check the configuration structure in `help-config.json`
2. Verify file paths exist in the repository
3. Test with the provided examples
4. Contact the development team for additional assistance
