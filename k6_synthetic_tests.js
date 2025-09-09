import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';

export let options = {
  stages: [
    { duration: '10s', target: 2 },
    { duration: '30s', target: 5 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.1'],
  },
};

// Base URL for the API
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8000';

// Test data
const testUsers = new SharedArray('test users', function () {
  return [
    { username: 'testuser1', email: 'test1@example.com', password: 'testpass123' },
    { username: 'testuser2', email: 'test2@example.com', password: 'testpass123' },
    { username: 'testuser3', email: 'test3@example.com', password: 'testpass123' },
  ];
});

let authToken = '';

export function setup() {
  // Create a test user for authentication
  const createUserPayload = {
    username: 'k6testuser',
    email: 'k6test@example.com',
    password: 'k6testpass123',
    password_confirm: 'k6testpass123'
  };

  const createUserResponse = http.post(
    `${BASE_URL}/api/access/users/`,
    JSON.stringify(createUserPayload),
    { headers: { 'Content-Type': 'application/json' } }
  );

  if (createUserResponse.status === 201) {
    console.log('Test user created successfully');
  }

  // Login to get auth token
  const loginPayload = {
    email: 'k6test@example.com',
    password: 'k6testpass123'
  };

  const loginResponse = http.post(
    `${BASE_URL}/api/access/auth/login/`,
    JSON.stringify(loginPayload),
    { headers: { 'Content-Type': 'application/json' } }
  );

  if (loginResponse.status === 200) {
    const token = JSON.parse(loginResponse.body).access;
    console.log('Authentication successful');
    return { token: token };
  } else {
    console.error('Authentication failed:', loginResponse.body);
    return { token: '' };
  }
}

export default function (data) {
  const headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${data.token}`
  };

  // Test 1: User Registration
  testUserRegistration();

  // Test 2: User Authentication
  testUserAuthentication();

  // Test 3: Protected Endpoints
  testProtectedEndpoints(headers);

  // Test 4: Pre-Registration (Public endpoint)
  testPreRegistration();

  // Test 5: Logged Devices CRUD
  testLoggedDevicesCRUD(headers);

  // Test 6: Reset Password Control
  testResetPasswordControl(headers);

  // Test 7: Email Confirmation Control
  testEmailConfirmationControl(headers);

  sleep(1);
}

function testUserRegistration() {
  const user = testUsers[Math.floor(Math.random() * testUsers.length)];
  const payload = {
    username: `${user.username}_${Date.now()}`,
    email: `${Date.now()}_${user.email}`,
    password: user.password,
    password_confirm: user.password
  };

  const response = http.post(
    `${BASE_URL}/api/access/users/`,
    JSON.stringify(payload),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(response, {
    'user registration status is 201': (r) => r.status === 201,
    'user registration response has userId': (r) => JSON.parse(r.body).userId !== undefined,
    'user registration response has email': (r) => JSON.parse(r.body).email === payload.email,
  });
}

function testUserAuthentication() {
  const loginPayload = {
    email: 'k6test@example.com',
    password: 'k6testpass123'
  };

  const response = http.post(
    `${BASE_URL}/api/access/auth/login/`,
    JSON.stringify(loginPayload),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(response, {
    'authentication status is 200': (r) => r.status === 200,
    'authentication response has access token': (r) => JSON.parse(r.body).access !== undefined,
    'authentication response has refresh token': (r) => JSON.parse(r.body).refresh !== undefined,
  });
}

function testProtectedEndpoints(headers) {
  // Test getting current user
  const currentUserResponse = http.get(`${BASE_URL}/api/access/users/me/`, { headers });

  check(currentUserResponse, {
    'current user status is 200': (r) => r.status === 200,
    'current user has email': (r) => JSON.parse(r.body).email === 'k6test@example.com',
  });

  // Test listing users
  const usersListResponse = http.get(`${BASE_URL}/api/access/users/`, { headers });

  check(usersListResponse, {
    'users list status is 200': (r) => r.status === 200,
    'users list has results': (r) => JSON.parse(r.body).results !== undefined,
  });
}

function testPreRegistration() {
  const payload = {
    email: `preregister_${Date.now()}@example.com`
  };

  const response = http.post(
    `${BASE_URL}/api/access/pre-register/`,
    JSON.stringify(payload),
    { headers: { 'Content-Type': 'application/json' } }
  );

  check(response, {
    'pre-registration status is 201': (r) => r.status === 201,
    'pre-registration response has email': (r) => JSON.parse(r.body).email === payload.email,
  });
}

function testLoggedDevicesCRUD(headers) {
  // Create logged device
  const devicePayload = {
    device_type: 'desktop',
    device_name: `K6 Test Browser ${Date.now()}`,
    place: 'K6 Test City'
  };

  const createResponse = http.post(
    `${BASE_URL}/api/access/logged-devices/`,
    JSON.stringify(devicePayload),
    { headers }
  );

  check(createResponse, {
    'device creation status is 201': (r) => r.status === 201,
    'device creation response has id': (r) => JSON.parse(r.body).id !== undefined,
  });

  if (createResponse.status === 201) {
    const deviceId = JSON.parse(createResponse.body).id;

    // Read logged device
    const readResponse = http.get(`${BASE_URL}/api/access/logged-devices/${deviceId}/`, { headers });

    check(readResponse, {
      'device read status is 200': (r) => r.status === 200,
      'device read response has device_name': (r) => JSON.parse(r.body).device_name === devicePayload.device_name,
    });

    // Update last login
    const updateLoginResponse = http.post(
      `${BASE_URL}/api/access/logged-devices/${deviceId}/update_login/`,
      null,
      { headers }
    );

    check(updateLoginResponse, {
      'device update login status is 200': (r) => r.status === 200,
    });

    // Delete logged device
    const deleteResponse = http.del(`${BASE_URL}/api/access/logged-devices/${deviceId}/`, { headers });

    check(deleteResponse, {
      'device deletion status is 204': (r) => r.status === 204,
    });
  }
}

function testResetPasswordControl(headers) {
  const payload = {
    email: `reset_${Date.now()}@example.com`
  };

  const response = http.post(
    `${BASE_URL}/api/access/reset-password-control/`,
    JSON.stringify(payload),
    { headers }
  );

  check(response, {
    'reset password control status is 201': (r) => r.status === 201,
    'reset password control has request_id': (r) => JSON.parse(r.body).request_id !== undefined,
  });
}

function testEmailConfirmationControl(headers) {
  const payload = {
    email: `confirm_${Date.now()}@example.com`
  };

  const response = http.post(
    `${BASE_URL}/api/access/email-confirmation-control/`,
    JSON.stringify(payload),
    { headers }
  );

  check(response, {
    'email confirmation control status is 201': (r) => r.status === 201,
    'email confirmation control has email': (r) => JSON.parse(r.body).email === payload.email,
  });
}

export function teardown(data) {
  // Cleanup could be performed here if needed
  console.log('K6 test completed');
}
