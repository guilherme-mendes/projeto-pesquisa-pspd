(defproject wordcount "0.0.1-SNAPSHOT"
  :resource-paths ["_resources"]
  :target-path "_build"
  :min-lein-version "2.0.0"
  :jvm-opts ["-client"]
  :dependencies  [[org.apache.storm/storm-core "2.4.0"]
                  [org.apache.storm/flux-core "2.4.0"]]
  :jar-exclusions     [#"log4j\.properties" #"trident" #"META-INF" #"meta-inf" #"\.yaml"]
  :uberjar-exclusions [#"log4j\.properties" #"trident" #"META-INF" #"meta-inf" #"\.yaml"]
  )
(require 'cemerick.pomegranate.aether)
(cemerick.pomegranate.aether/register-wagon-factory!
 "http" #(org.apache.maven.wagon.providers.http.HttpWagon.))