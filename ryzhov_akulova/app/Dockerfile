FROM rust:1 AS builder

WORKDIR /app

COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN cargo build --release

FROM debian:bookworm-slim

WORKDIR /app

COPY --from=builder /app/target/release/recipes_api /app/recipes_api

EXPOSE 3000

CMD ["./recipes_api"]