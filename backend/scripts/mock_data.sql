-- This script inserts mock data for testing the statistics features.
-- It's recommended to run this on a development or testing database.

-- NOTE: This script assumes a user with id=1 and exercises with ids=1 and 2 already exist.
-- If your exercise IDs are different, please update the 'exercise_id' values in the logs section below.

-- To ensure a clean slate, you can optionally clear existing data.
-- Be careful with these commands on a database with important data.
/*
DELETE FROM user_exercise_logs;
DELETE FROM workout_exercises;
DELETE FROM workouts;
DELETE FROM exercises;
DELETE FROM users;
*/

-- 1. Insert a mock user (Commented out as user with id=1 is assumed to exist)
/*
-- We'll use user_id = 1 for all subsequent data.
INSERT INTO users (id, username, email, hashed_password, created_at, updated_at) VALUES
(1, 'mock_user', 'mock@test.com', 'some_hashed_password_that_is_not_important_for_this_script', '2023-01-01 10:00:00', '2023-01-01 10:00:00')
ON CONFLICT (id) DO NOTHING;
*/

-- 2. Insert some common exercises (Commented out as exercises are assumed to exist)
/*
INSERT INTO exercises (id, name, description, muscle_group, is_cardio) VALUES
(1, 'Bench Press', 'Lying on a bench, pushing a weight upwards.', 'Chest', false),
(2, 'Squat', 'Lowering hips from a standing position and then standing back up.', 'Legs', false),
(3, 'Deadlift', 'Lifting a loaded barbell off the ground to the level of the hips.', 'Back', false)
ON CONFLICT (id) DO NOTHING;
*/

-- 3. Insert a few workout sessions for the user to show progression over time
-- The dates are spread out to test the time-based graphs.
INSERT INTO workouts (id, user_id, name, date) VALUES
(1, 1, 'Push Day 1', '2024-05-01'),
(2, 1, 'Leg Day', '2024-05-03'),
(3, 1, 'Push Day 2', '2024-05-08')
ON CONFLICT (id) DO NOTHING;

-- 4. Insert user exercise logs
-- These logs represent the actual sets performed by the user.
-- The 'date' column should reflect the day the workout was done.

-- Logs for Workout 1: Push Day 1 (Bench Press @ 60kg)
INSERT INTO user_exercise_logs (user_id, exercise_id, workout_id, date, set_number, reps, weight, created_at) VALUES
(1, 1, 1, '2024-05-01 10:05:00', 1, 8, 60.0, '2024-05-01 10:05:00'),
(1, 1, 1, '2024-05-01 10:07:00', 2, 8, 60.0, '2024-05-01 10:07:00'),
(1, 1, 1, '2024-05-01 10:09:00', 3, 7, 60.0, '2024-05-01 10:09:00');

-- Logs for Workout 2: Leg Day (Squat @ 80kg)
INSERT INTO user_exercise_logs (user_id, exercise_id, workout_id, date, set_number, reps, weight, created_at) VALUES
(1, 2, 2, '2024-05-03 10:05:00', 1, 10, 80.0, '2024-05-03 10:05:00'),
(1, 2, 2, '2024-05-03 10:08:00', 2, 10, 80.0, '2024-05-03 10:08:00'),
(1, 2, 2, '2024-05-03 10:11:00', 3, 9, 80.0, '2024-05-03 10:11:00');

-- Logs for Workout 3: Push Day 2 (Bench Press @ 65kg - PROGRESSION!)
-- This second set of logs for Bench Press shows an increase in weight.
INSERT INTO user_exercise_logs (user_id, exercise_id, workout_id, date, set_number, reps, weight, created_at) VALUES
(1, 1, 3, '2024-05-08 10:06:00', 1, 8, 65.0, '2024-05-08 10:06:00'),
(1, 1, 3, '2024-05-08 10:08:00', 2, 7, 65.0, '2024-05-08 10:08:00'),
(1, 1, 3, '2024-05-08 10:10:00', 3, 6, 65.0, '2024-05-08 10:10:00');
