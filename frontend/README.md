# Artificial-Me Frontend

A modern React application built with TypeScript, Vite, and Ant Design. This frontend application provides a user interface for the Artificial-Me project.

## 🚀 Features

- Built with React 19 and TypeScript
- Modern UI components using Ant Design
- Dark mode support
- Markdown rendering capabilities
- Tailwind CSS for styling
- Docker support for development and production

## 🛠️ Tech Stack

- **Framework**: React 19
- **Language**: TypeScript
- **Build Tool**: Vite
- **UI Library**: Ant Design
- **Styling**: Tailwind CSS
- **Markdown**: markdown-to-jsx
- **Development**: ESLint, TypeScript

## 📦 Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

## 🚀 Development

To start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## 🏗️ Building for Production

To build the application for production:

```bash
npm run build
```

The built files will be in the `dist` directory.

## 🐳 Docker Support

### Development
```bash
docker build -f Dockerfile.dev -t artificial-me-frontend:dev .
docker run -p 5173:5173 artificial-me-frontend:dev
```

### Production
```bash
docker build -t artificial-me-frontend:prod .
docker run -p 80:80 artificial-me-frontend:prod
```

## 🔍 Code Quality

The project uses ESLint for code quality. To run linting:

```bash
npm run lint
```

## 📝 Environment Variables

Create a `.env` file based on `.env.example` with your configuration.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
