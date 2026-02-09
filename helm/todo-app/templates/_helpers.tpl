{{/*
Common labels for all resources
*/}}
{{- define "todo-app.labels" -}}
app: todo-app
chart: {{ .Chart.Name }}-{{ .Chart.Version }}
managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Backend selector labels
*/}}
{{- define "todo-app.backend.selectorLabels" -}}
app: todo-app
component: backend
{{- end -}}

{{/*
Frontend selector labels
*/}}
{{- define "todo-app.frontend.selectorLabels" -}}
app: todo-app
component: frontend
{{- end -}}
