# Fitness Tracker for Gym

## Overview
The **Fitness Tracker** is a Django-based web application designed to help gym enthusiasts log and manage their fitness routines. This system simplifies workout tracking by offering features for creating reusable workout templates, logging workout sessions, and organizing exercises with detailed instructions.


## Key Features

### 1. Routine Management
- **Routine**: A reusable workout template that users can create for workouts they plan to perform repeatedly.  
- Routines are a framework for organizing related workouts and streamlining future workout sessions.

### 2. **Workout Tracking**
- **Workout**: Represents a specific instance of exercise activity that a user is currently performing.  
- Each workout can consist of multiple sets, and each set includes:
  - **Weight**: The weight to be used for the exercise.
  - **Repetition**: The number of times the user will perform the exercise with the specified weight.  
- Workouts are based on **Exercises**, such as Chest Press Machine, Triceps Pushdown Machine, or Lat Pulldown.  
- Each exercise comes with detailed instructions to guide users on the correct technique and form.


## User Roles and Permissions

### 1. **Staff Users**
- Manage the exercise database:
  - Add, update, and delete exercises.
  - Provide detailed instructions steps for each exercise.

### 2. **Regular Users**
- **Routine Management**:
  - Create, update, and delete routines.
  - View their personal routines on a dedicated page, accessible only to the user.  
- **Workout Management**:
  - Add workouts to routines.
  - Edit or update workout details, including sets, weights, and repetitions.
- **Exercise Access**:
  - Browse the available exercises on a public page.
  - View detailed instructions for exercises but it requires user registration.


## Additional Features
- **Public Routines**: A  list of routines that all users can explore and benefit from them.


## Use Case
- **For Gym Enthusiasts**: Track weightlifting sessions, create routines, and follow guided instructions for exercises.

