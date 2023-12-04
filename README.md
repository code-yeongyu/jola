<p align="center">
  <img src="https://raw.githubusercontent.com/code-yeongyu/jola/master/docs/images/logo.png" alt="JOLA">
</p>
<p align="center">
    <em>Judicious Observant Linting Assistant</em>
</p>

# JOLA - Judicious Observant Linting Assistant 🚀

## Introduction

Welcome to JOLA, a groundbreaking Python linter!

JOLA stands out in the Python development landscape as it focuses on an often-overlooked yet crucial aspect: **Django relationship fields type hinting**.

### Why JOLA?

JOLA currently fills a critical gap in Django development. The typical Language Server Protocols (LSPs) struggle, especially with relationship fields like `ForeignKey` and `OneToOneField`. JOLA not only detects missing type hints in these areas but also offers a `--fix` option to automatically rectify them.

But that's just the beginning! 🌟 JOLA is set to evolve with more incredible features. Future updates will include capabilities like auto-generating explicit imports, further simplifying and streamlining your Django development process. Stay tuned for these exciting enhancements!

## Features

### 🕵️‍♂️ Detect Missing Type Hints of Relationship Fields

Consider the following Django model:

```python
class Article(models.Model):
    user = models.ForeignKey(User, ...)
```

In this case, LSPs often can't comprehend what `article.user.email` means. JOLA detects such instances and helps in maintaining robust type hinting.

#### 🛠️ Automatic Fix with `--fix`

JOLA doesn't just point out issues; it fixes them! With the `--fix` option, JOLA can automatically add appropriate type hints, turning your code into:

```python
class Article(models.Model):
    user: models.ForeignKey[User] = models.ForeignKey(User, ...)
```

Now, your IDE understands exactly what `article.user.email` refers to!

#### 🔗 Leverage Deep Relationships

JOLA shines in complex scenarios involving nested relationships. For example:

```python
class Profile(models.Model):
    image_url = models.ImageField(...)

class User(models.Model):
    profile: models.OneToOneField[Profile] = models.OneToOneField(Profile, ...)

class Article(models.Model):
    user: models.ForeignKey[User] = models.ForeignKey(User, ...)
```

Here, JOLA ensures that even deeply nested attributes like `article.user.profile.image_url` are clearly understood by your language server.

#### Limitations and Workarounds

While JOLA is powerful, it has its limitations. For instance, when a `ForeignKey` is not directly defined with the actual model, JOLA cannot automatically fix it:

```python
class Article(models.Model):
    user = models.ForeignKey('users.User', ...)
```

In such cases, JOLA recommends a workaround to avoid circular imports and maintain clarity:

```python
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from users.models import User
else:
    User = Any

class Article(models.Model):
    user = models.ForeignKey('users.User', ...)
```

This approach ensures type hinting for language servers without runtime import issues.

## Installation

Currently, JOLA is available only for Python 3.9+.

Sadly, JOLA is not yet available on PyPI. I am working on it and this section will be updated once it is available.
