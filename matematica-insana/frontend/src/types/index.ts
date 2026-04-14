export type UserRole = "student" | "teacher" | "admin";

export type GradeLevel =
  | "6ano" | "7ano" | "8ano" | "9ano"
  | "1em" | "2em" | "3em"
  | "vestibular" | "concurso";

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  grade_level: GradeLevel | null;
  avatar_url: string | null;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export type DifficultyLevel = "abaixo_basico" | "basico" | "adequado" | "avancado";
export type MathTopic =
  | "numeros_e_operacoes"
  | "algebra"
  | "geometria"
  | "estatistica_e_probabilidade"
  | "grandezas_e_medidas"
  | "raciocinio_logico";

export interface ExerciseOption {
  id: string;
  text: string;
}

export interface Exercise {
  id: string;
  title: string;
  statement: string;
  options: ExerciseOption[] | null;
  difficulty: DifficultyLevel;
  topic: MathTopic;
  subtopic: string | null;
  grade_levels: string[];
  bloom_level: number | null;
  exam_source: string;
  exam_year: number | null;
  created_at: string;
}

export interface ExerciseAttemptResponse {
  id: string;
  exercise_id: string;
  answer: string;
  is_correct: boolean;
  correct_answer: string;
  explanation: string | null;
  xp_earned: number;
  created_at: string;
}

export interface DiagnosticResult {
  id: string;
  user_id: string;
  grade_level: string;
  status: "em_andamento" | "concluido";
  scores: Record<string, { score: number; level: string }>;
  gaps: Array<{ topic: string; score: number; level: string; priority: number }>;
  learning_path: Array<{ topic: string; level: string; priority: number; estimated_hours: number }>;
  total_questions: number;
  correct_answers: number;
  overall_score: number | null;
  overall_level: string | null;
  started_at: string;
  completed_at: string | null;
}

export interface Gamification {
  user_id: string;
  xp: number;
  level: number;
  streak_days: number;
  total_exercises: number;
  correct_exercises: number;
  accuracy: number;
  achievements: string[];
}
