@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Examination Management System - C4 Architecture Diagram

' ========== Colors and Styling ==========
skinparam {
    shadowing true
    arrowColor #3689d1
    actorBorderColor #444
    componentBorderColor #444
    componentBackgroundColor #f0f8ff
    databaseBorderColor #444
    databaseBackgroundColor #e6f3ff
    defaultFontName Arial
    titleFontSize 16
    footerFontSize 10
}

' ========== People and Systems ==========
Person(admin, "Administrator", "Manages system configuration and users")
Person(lecturer, "Lecturer", "Views schedule, reports conflicts")
Person(student, "Student", "Views exam timetable")
Person(committee, "Examination Committee", "Generates reports, oversees process")

System_Boundary(system, "Examination Management System") {

    ' ========== Containers ==========
    Container(web_app, "Web Application", "Django", "Provides all system functionality through web interface")
    Container(mobile_app, "Mobile App", "React Native", "Mobile access for invigilators")
    Container(db, "Database", "PostgreSQL", "Stores all system data")
    Container(redis, "Cache & Message Broker", "Redis", "Handles real-time notifications")
    Container(export_service, "Export Service", "Python", "Generates PDF/CSV/Excel reports")
    
    ' ========== Web App Components ==========
    Container_Boundary(web_app_boundary, "Web Application Components") {
        Component(auth, "Authentication", "Django Auth", "Handles user login, permissions")
        Component(scheduling, "Scheduling Engine", "Python", "Manages exam scheduling logic")
        Component(conflict, "Conflict Detection", "Python", "Identifies scheduling conflicts")
        Component(notification, "Notification Service", "Django Channels", "Real-time alerts")
        Component(api, "REST API", "Django REST", "Provides data to mobile app")
        Component(ui, "User Interface", "HTML/JS", "Web frontend")
    }
    
    ' ========== Mobile App Components ==========
    Container_Boundary(mobile_boundary, "Mobile App Components") {
        Component(mobile_ui, "Mobile UI", "React Native", "User interface")
        Component(mobile_sync, "Sync Service", "React Native", "Offline data sync")
    }
}

' ========== Relationships ==========
Rel(admin, web_app, "Manages system configuration", "HTTPS")
Rel(lecturer, web_app, "Views schedule, reports issues", "HTTPS")
Rel(lecturer, mobile_app, "Checks assignments on-the-go", "HTTPS")
Rel(student, web_app, "Views exam timetable", "HTTPS")
Rel(committee, web_app, "Generates reports", "HTTPS")

Rel(web_app, db, "Reads/Writes data", "JDBC")
Rel(web_app, redis, "Publishes notifications", "WebSocket")
Rel(web_app, export_service, "Requests reports", "HTTP")
Rel(mobile_app, api, "Syncs data", "REST/HTTPS")
Rel(api, db, "Queries data", "JDBC")
Rel(notification, redis, "Subscribes to events", "Pub/Sub")

' ========== Internal Web App Relationships ==========
Rel(ui, auth, "Authenticates users", "HTTPS")
Rel(ui, scheduling, "Creates/Edits exams", "HTTPS")
Rel(scheduling, conflict, "Checks for conflicts", "RPC")
Rel(conflict, notification, "Sends conflict alerts", "Event")
Rel(notification, ui, "Pushes real-time updates", "WebSocket")

' ========== Deployment View ==========
Deployment_Node(server, "Cloud Server", "Ubuntu 20.04", "AWS EC2") {
    Container(web_app)
    Container(db)
    Container(redis)
    Container(export_service)
}

Deployment_Node(cdn, "CDN", "CloudFront", "AWS CDN") {
    Container(ui)
}

Deployment_Node(mobile, "Mobile Devices", "iOS/Android") {
    Container(mobile_app)
}

' ========== Legend ==========
legend right
  | Color | Meaning |
  | <#FFAAAA> | People |
  | <#AAFFAA> | Systems |
  | <#FFFFAA> | Containers |
  | <#DAA520> | Components |
  | <#ADD8E6> | Deployment Nodes |
end legend

footer Examination System Architecture v1.0 | Generated on %date("yyyy-MM-dd")%
@enduml