#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('🚀 FlavorGraph Deployment Helper\n');

// Check if .env.local exists
const envPath = path.join(__dirname, '.env.local');
if (!fs.existsSync(envPath)) {
  console.error('❌ .env.local file not found!');
  console.log('Please create .env.local with your Supabase credentials.');
  process.exit(1);
}

// Read environment variables
const envContent = fs.readFileSync(envPath, 'utf8');
const hasSupabaseUrl = envContent.includes('NEXT_PUBLIC_SUPABASE_URL=https://');
const hasSupabaseKey = envContent.includes('NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ');

if (!hasSupabaseUrl || !hasSupabaseKey) {
  console.error('❌ Supabase configuration incomplete!');
  console.log('Please check your .env.local file has proper Supabase URL and key.');
  process.exit(1);
}

console.log('✅ Environment variables configured');

// Clean build
console.log('🧹 Cleaning previous build...');
try {
  execSync('rm -rf .next', { stdio: 'inherit' });
} catch (error) {
  // Ignore error if .next doesn't exist
}

// Install dependencies
console.log('📦 Installing dependencies...');
try {
  execSync('npm install --legacy-peer-deps', { stdio: 'inherit' });
  console.log('✅ Dependencies installed');
} catch (error) {
  console.error('❌ Failed to install dependencies');
  console.log('Try running: npm cache clean --force && npm install');
  process.exit(1);
}

// Build project
console.log('🔨 Building project...');
try {
  execSync('npm run build', { stdio: 'inherit' });
  console.log('✅ Build successful!');
} catch (error) {
  console.error('❌ Build failed');
  console.log('Check the error messages above and fix any issues.');
  process.exit(1);
}

// Test production build
console.log('🧪 Testing production build...');
console.log('Starting production server on http://localhost:3000');
console.log('Press Ctrl+C to stop the server when testing is complete.\n');

try {
  execSync('npm start', { stdio: 'inherit' });
} catch (error) {
  console.log('\n✅ Production test completed');
}

console.log('\n🎉 Your FlavorGraph app is ready for deployment!');
console.log('\nNext steps:');
console.log('1. Choose a deployment platform (Vercel, Netlify, Railway)');
console.log('2. Set up environment variables on the platform');
console.log('3. Deploy your application');
console.log('4. Update Supabase redirect URLs with your production domain');
console.log('\nSee DEPLOYMENT_GUIDE.md for detailed instructions.');
