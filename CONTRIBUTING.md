# Contributing to MindMate

Thank you for your interest in contributing to MindMate! This document provides guidelines for contributing to the project.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or identity.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Prioritize user safety and mental health

### Unacceptable Behavior

- Harassment or discrimination of any kind
- Trolling or inflammatory comments
- Sharing private information without consent
- Any behavior that could harm users' mental health

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, etc.)
   - Screenshots if applicable

### Suggesting Features

1. Check existing issues and discussions
2. Create a feature request with:
   - Clear use case
   - Expected behavior
   - Potential implementation approach
   - Consider ethical implications

### Code Contributions

#### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/AI-ChatBot.git
cd AI-ChatBot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

#### Development Workflow

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes**
   - Follow coding standards (see below)
   - Add tests for new features
   - Update documentation

3. **Test your changes**
   ```bash
   # Run tests
   pytest
   
   # Run linter
   flake8 .
   
   # Format code
   black .
   
   # Type checking
   mypy app.py
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```
   
   Use conventional commit messages:
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation changes
   - `test:` adding tests
   - `refactor:` code refactoring
   - `style:` formatting changes
   - `chore:` maintenance tasks

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where possible
- Maximum line length: 100 characters
- Use docstrings for functions and classes
- Format with `black`

Example:
```python
def detect_emotion(text: str) -> str:
    """
    Detect emotion from user text.
    
    Args:
        text: User input message
        
    Returns:
        Detected emotion label
    """
    # Implementation
    pass
```

### JavaScript/React (Frontend)

- Use ES6+ syntax
- Functional components with hooks
- PropTypes or TypeScript for type checking
- Use ESLint configuration
- Format with Prettier

Example:
```javascript
const ChatMessage = ({ message, emotion, crisis }) => {
  return (
    <div className={`message ${emotion}`}>
      {message}
    </div>
  );
};
```

### Testing

- Write tests for new features
- Maintain test coverage >80%
- Test edge cases and error handling
- Include integration tests for API endpoints

Example:
```python
def test_emotion_detection():
    """Test emotion detection with sample inputs."""
    assert detect_emotion("I'm so happy!") == "joy"
    assert detect_emotion("I feel sad") == "sadness"
```

## Special Considerations for Mental Health AI

### Safety First

1. **Crisis Detection**
   - Never reduce crisis detection sensitivity
   - Test thoroughly with diverse crisis expressions
   - Ensure 100% recall for critical cases
   - Always provide helpline information

2. **Ethical Response Generation**
   - Avoid giving medical advice
   - Don't make promises or guarantees
   - Maintain empathetic but professional tone
   - Include appropriate disclaimers

3. **Privacy & Security**
   - Never log sensitive user data without consent
   - Implement proper data encryption
   - Follow GDPR/HIPAA guidelines
   - Anonymize data for research

### Testing Mental Health Features

When testing crisis detection or emotional responses:

1. Use synthetic test data, not real crisis messages
2. Consult mental health professionals for validation
3. Test with diverse cultural contexts
4. Verify helpline information is accurate and up-to-date

## Documentation

### Code Documentation

- Add docstrings to all functions and classes
- Include type hints
- Explain complex logic with comments
- Update README.md for user-facing changes

### API Documentation

- Document all endpoints
- Include request/response examples
- Note error codes and handling
- Update OpenAPI/Swagger specs

## Pull Request Process

1. **Before Submitting**
   - [ ] Code follows style guidelines
   - [ ] Tests pass locally
   - [ ] Documentation updated
   - [ ] No merge conflicts
   - [ ] Commits are clean and descriptive

2. **PR Description**
   - Clear title summarizing changes
   - Detailed description of what and why
   - Link related issues
   - Screenshots for UI changes
   - Note breaking changes

3. **Review Process**
   - Maintainers will review within 3-5 days
   - Address feedback and comments
   - Keep PR focused and small
   - Be patient and respectful

4. **Merging**
   - Requires approval from maintainer
   - All tests must pass
   - No unresolved conversations
   - Squash commits if requested

## Areas for Contribution

### High Priority

- [ ] Multi-language support (Hindi, Spanish, etc.)
- [ ] Improved crisis detection patterns
- [ ] Better evaluation metrics
- [ ] Performance optimization
- [ ] Accessibility improvements

### Medium Priority

- [ ] User authentication system
- [ ] Persistent storage (Redis/PostgreSQL)
- [ ] Admin dashboard
- [ ] Advanced analytics
- [ ] Mobile app (React Native)

### Documentation

- [ ] Video tutorials
- [ ] API documentation
- [ ] Deployment guides
- [ ] Translation of docs

### Research

- [ ] Fine-tuning on therapy datasets
- [ ] Bias detection and mitigation
- [ ] Multi-modal emotion detection
- [ ] Personalization algorithms

## Getting Help

- **Questions:** Open a discussion on GitHub
- **Bugs:** Create an issue
- **Security:** Email maintainers directly
- **General:** Join community chat

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in academic publications (if applicable)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make MindMate better! 🧠❤️
